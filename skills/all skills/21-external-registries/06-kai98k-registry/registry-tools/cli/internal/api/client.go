package api

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
)

type Client struct {
	baseURL    string
	token      string
	httpClient *http.Client
}

type PublishResult struct {
	Name        string `json:"name"`
	Version     string `json:"version"`
	Checksum    string `json:"checksum"`
	PublishedAt string `json:"published_at"`
}

type SkillInfo struct {
	Name          string        `json:"name"`
	Owner         string        `json:"owner"`
	Downloads     int64         `json:"downloads"`
	LatestVersion VersionInfo   `json:"latest_version"`
}

type VersionInfo struct {
	Version     string `json:"version"`
	Description string `json:"description"`
	Checksum    string `json:"checksum"`
	SizeBytes   int64  `json:"size_bytes"`
	PublishedAt string `json:"published_at"`
}

type SearchResult struct {
	Total   int            `json:"total"`
	Page    int            `json:"page"`
	PerPage int            `json:"per_page"`
	Results []SearchEntry  `json:"results"`
}

type SearchEntry struct {
	Name          string   `json:"name"`
	Description   string   `json:"description"`
	Owner         string   `json:"owner"`
	Downloads     int64    `json:"downloads"`
	LatestVersion string   `json:"latest_version"`
	Tags          []string `json:"tags"`
}

func NewClient(baseURL, token string) *Client {
	return &Client{
		baseURL:    baseURL,
		token:      token,
		httpClient: &http.Client{},
	}
}

func (c *Client) Publish(bundlePath string) (*PublishResult, error) {
	f, err := os.Open(bundlePath)
	if err != nil {
		return nil, fmt.Errorf("opening bundle: %w", err)
	}
	defer f.Close()

	// Create multipart request
	pr, pw := io.Pipe()
	writer := newMultipartWriter(pw, filepath.Base(bundlePath), f)

	req, err := http.NewRequest("POST", c.baseURL+"/v1/skills/publish", pr)
	if err != nil {
		return nil, fmt.Errorf("creating request: %w", err)
	}
	req.Header.Set("Authorization", "Bearer "+c.token)
	req.Header.Set("Content-Type", writer.contentType)

	go writer.write()

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("sending request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("server returned %d: %s", resp.StatusCode, string(body))
	}

	var result PublishResult
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decoding response: %w", err)
	}
	return &result, nil
}

func (c *Client) GetSkill(name string) (*SkillInfo, error) {
	resp, err := c.httpClient.Get(c.baseURL + "/v1/skills/" + url.PathEscape(name))
	if err != nil {
		return nil, fmt.Errorf("fetching skill: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		return nil, fmt.Errorf("skill %q not found", name)
	}
	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("server returned %d: %s", resp.StatusCode, string(body))
	}

	var info SkillInfo
	if err := json.NewDecoder(resp.Body).Decode(&info); err != nil {
		return nil, fmt.Errorf("decoding response: %w", err)
	}
	return &info, nil
}

func (c *Client) Download(name, version string) (tmpFile string, checksum string, err error) {
	u := fmt.Sprintf("%s/v1/skills/%s/versions/%s/download",
		c.baseURL, url.PathEscape(name), url.PathEscape(version))

	resp, err := c.httpClient.Get(u)
	if err != nil {
		return "", "", fmt.Errorf("downloading: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return "", "", fmt.Errorf("server returned %d: %s", resp.StatusCode, string(body))
	}

	checksum = resp.Header.Get("X-Checksum-SHA256")

	f, err := os.CreateTemp("", "agentskills-*.tar.gz")
	if err != nil {
		return "", "", fmt.Errorf("creating temp file: %w", err)
	}
	defer f.Close()

	if _, err := io.Copy(f, resp.Body); err != nil {
		os.Remove(f.Name())
		return "", "", fmt.Errorf("writing download: %w", err)
	}

	return f.Name(), checksum, nil
}

func (c *Client) Search(keyword string) (*SearchResult, error) {
	u := fmt.Sprintf("%s/v1/skills?q=%s", c.baseURL, url.QueryEscape(keyword))
	resp, err := c.httpClient.Get(u)
	if err != nil {
		return nil, fmt.Errorf("searching: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("server returned %d: %s", resp.StatusCode, string(body))
	}

	var result SearchResult
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decoding response: %w", err)
	}
	return &result, nil
}

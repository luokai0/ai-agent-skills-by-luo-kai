package api

import (
	"io"
	"mime/multipart"
)

type multipartPipe struct {
	pw          *io.PipeWriter
	reader      io.Reader
	filename    string
	contentType string
	writer      *multipart.Writer
}

func newMultipartWriter(pw *io.PipeWriter, filename string, reader io.Reader) *multipartPipe {
	w := multipart.NewWriter(pw)
	return &multipartPipe{
		pw:          pw,
		reader:      reader,
		filename:    filename,
		contentType: w.FormDataContentType(),
		writer:      w,
	}
}

func (m *multipartPipe) write() {
	defer func() {
		m.writer.Close()
		m.pw.Close()
	}()

	part, err := m.writer.CreateFormFile("file", m.filename)
	if err != nil {
		m.pw.CloseWithError(err)
		return
	}

	if _, err := io.Copy(part, m.reader); err != nil {
		m.pw.CloseWithError(err)
		return
	}
}

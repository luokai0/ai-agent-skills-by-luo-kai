#!/usr/bin/env bun
/**
 * Step 3: Record narration with ElevenLabs, get word-level timestamps
 */

import { parseArgs } from "util";
import { backupBeforeWrite } from "./lib/versioning";

interface NarrationScene {
  id: string;
  type: string;
  narrationText: string;
  relatedPostIndices: number[];
  visualDirection: string;
}

interface NarrationScript {
  title: string;
  handle: string;
  scenes: NarrationScene[];
  fullNarration: string;
}

interface WordTimestamp {
  word: string;
  start: number;
  end: number;
}

interface SceneTimestamp {
  sceneId: string;
  start: number;
  end: number;
  words: WordTimestamp[];
}

interface AudioManifest {
  audioPath: string;
  duration: number;
  voiceId: string;
  voiceName: string;
  scenes: SceneTimestamp[];
  words: WordTimestamp[];
}

async function findDocumentaryVoice(apiKey: string): Promise<{ id: string; name: string }> {
  const preferredVoices = [
    { id: "JBFqnCBsd6RMkjVDRZzb", name: "George" },
    { id: "TxGEqnHWrfWFTfGW9XjX", name: "Josh" },
    { id: "pNInz6obpgDQGcFmaJgB", name: "Adam" },
  ];

  try {
    const response = await fetch("https://api.elevenlabs.io/v1/voices", {
      headers: { "xi-api-key": apiKey },
    });

    if (response.ok) {
      const data = (await response.json()) as { voices: Array<{ voice_id: string; name: string }> };
      for (const pref of preferredVoices) {
        const found = data.voices.find((v) => v.voice_id === pref.id);
        if (found) return { id: found.voice_id, name: found.name };
      }
      if (data.voices.length > 0) {
        return { id: data.voices[0].voice_id, name: data.voices[0].name };
      }
    }
  } catch (e) {
    console.warn("Could not fetch voice list, using default");
  }

  return preferredVoices[0];
}

async function synthesizeWithTimestamps(
  text: string,
  voiceId: string,
  apiKey: string
): Promise<{ audio: ArrayBuffer; alignment: { characters: string[]; character_start_times_seconds: number[]; character_end_times_seconds: number[] } }> {
  const response = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/with-timestamps`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "xi-api-key": apiKey,
      },
      body: JSON.stringify({
        text,
        model_id: "eleven_multilingual_v2",
        voice_settings: {
          stability: 0.65,
          similarity_boost: 0.75,
          style: 0.35,
          use_speaker_boost: true,
        },
      }),
    }
  );

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`ElevenLabs API error: ${error}`);
  }

  const data = await response.json() as {
    audio_base64: string;
    alignment: {
      characters: string[];
      character_start_times_seconds: number[];
      character_end_times_seconds: number[];
    };
  };

  const audioBuffer = Uint8Array.from(atob(data.audio_base64), (c) => c.charCodeAt(0));
  
  return {
    audio: audioBuffer.buffer,
    alignment: data.alignment,
  };
}

function alignmentToWords(
  text: string,
  alignment: { characters: string[]; character_start_times_seconds: number[]; character_end_times_seconds: number[] }
): WordTimestamp[] {
  const words: WordTimestamp[] = [];
  let currentWord = "";
  let wordStart = 0;
  let wordEnd = 0;

  for (let i = 0; i < alignment.characters.length; i++) {
    const char = alignment.characters[i];
    const charStart = alignment.character_start_times_seconds[i];
    const charEnd = alignment.character_end_times_seconds[i];

    if (char === " " || char === "\n") {
      if (currentWord.trim()) {
        words.push({
          word: currentWord.trim(),
          start: wordStart,
          end: wordEnd,
        });
      }
      currentWord = "";
      wordStart = charEnd;
    } else {
      if (!currentWord) {
        wordStart = charStart;
      }
      currentWord += char;
      wordEnd = charEnd;
    }
  }

  if (currentWord.trim()) {
    words.push({
      word: currentWord.trim(),
      start: wordStart,
      end: wordEnd,
    });
  }

  return words;
}

function mapWordsToScenes(
  script: NarrationScript,
  words: WordTimestamp[]
): SceneTimestamp[] {
  const sceneTimestamps: SceneTimestamp[] = [];
  let wordIndex = 0;

  for (const scene of script.scenes) {
    const sceneWords = scene.narrationText.split(/\s+/).filter(Boolean);
    const sceneWordTimestamps: WordTimestamp[] = [];
    
    let sceneStart = words[wordIndex]?.start ?? 0;
    let sceneEnd = sceneStart;

    for (let i = 0; i < sceneWords.length && wordIndex < words.length; i++) {
      sceneWordTimestamps.push(words[wordIndex]);
      sceneEnd = words[wordIndex].end;
      wordIndex++;
    }

    sceneTimestamps.push({
      sceneId: scene.id,
      start: sceneStart,
      end: sceneEnd,
      words: sceneWordTimestamps,
    });
  }

  return sceneTimestamps;
}

async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      script: { type: "string", short: "s" },
      output: { type: "string", short: "o" },
    },
    allowPositionals: true,
  });

  const scriptPath = values.script || positionals[0];
  if (!scriptPath) {
    console.error("Usage: bun run record-audio.ts --script <script.json>");
    process.exit(1);
  }

  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) {
    throw new Error("ELEVENLABS_API_KEY not set. Add it in Settings > Developers.");
  }

  console.log(`📖 Loading script from ${scriptPath}...`);
  const script = (await Bun.file(scriptPath).json()) as NarrationScript;

  // Reconstruct fullNarration from scenes to ensure single source of truth
  const fullNarration = script.scenes
    .map((s) => s.narrationText)
    .join("\n\n");

  console.log(`🎭 Selecting voice...`);
  const voice = await findDocumentaryVoice(apiKey);
  console.log(`   Using: ${voice.name}`);

  console.log(`🎙️  Recording narration with timestamps...`);
  const { audio, alignment } = await synthesizeWithTimestamps(
    fullNarration,
    voice.id,
    apiKey
  );

  const words = alignmentToWords(fullNarration, alignment);
  const sceneTimestamps = mapWordsToScenes(script, words);
  
  const duration = words.length > 0 ? words[words.length - 1].end : 0;

  const outputDir = scriptPath.replace("/script.json", "");
  const audioPath = values.output || `${outputDir}/narration.mp3`;
  
  // Backup existing files before overwriting
  const audioBackup = await backupBeforeWrite(audioPath);
  if (audioBackup) {
    console.log(`📦 Previous audio backed up to: ${audioBackup}`);
  }
  
  await Bun.write(audioPath, audio);
  console.log(`💾 Audio saved: ${audioPath}`);

  const manifest: AudioManifest = {
    audioPath,
    duration,
    voiceId: voice.id,
    voiceName: voice.name,
    scenes: sceneTimestamps,
    words,
  };

  const manifestPath = audioPath.replace(".mp3", "-timestamps.json");
  
  const timestampBackup = await backupBeforeWrite(manifestPath);
  if (timestampBackup) {
    console.log(`📦 Previous timestamps backed up to: ${timestampBackup}`);
  }
  
  await Bun.write(manifestPath, JSON.stringify(manifest, null, 2));
  
  console.log(`\n✅ Recording complete!`);
  console.log(`   Audio: ${audioPath}`);
  console.log(`   Duration: ${duration.toFixed(1)}s`);
  console.log(`   Timestamps: ${manifestPath}`);
  console.log(`   Words tracked: ${words.length}`);
  
  console.log(`\n📊 Scene breakdown:`);
  for (const scene of sceneTimestamps) {
    console.log(`   [${scene.start.toFixed(1)}s - ${scene.end.toFixed(1)}s] ${scene.sceneId}`);
  }
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});

import { Config } from "@remotion/cli/config";

// Fast intermediate frames
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(80);

// Always overwrite
Config.setOverwriteOutput(true);

// H.264 with reasonable quality
Config.setCodec("h264");
Config.setCrf(23);

// Parallel rendering - adjust based on RAM (4-8 is usually good)
Config.setConcurrency(4);

// Reduce Chrome overhead
Config.setChromiumDisableWebSecurity(true);

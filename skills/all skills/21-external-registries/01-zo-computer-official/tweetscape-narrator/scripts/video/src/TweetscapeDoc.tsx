import React from "react";
import {
  Composition,
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Audio,
  Img,
  staticFile,
} from "remotion";

interface SceneTimestamp {
  sceneId: string;
  start: number;
  end: number;
}

interface Post {
  text: string;
  author: { handle: string; displayName?: string };
  likeCount: number;
  replyCount: number;
  isReply: boolean;
  screenshotPath?: string;
}

interface VideoProps {
  audioPath: string;
  scenes: SceneTimestamp[];
  posts: Post[];
  profileScreenshot?: string;
  profileName: string;
  handle: string;
  duration: number;
  relatedPostsByScene: { [sceneId: string]: number[] };
  focusPointsByScene?: { [sceneId: string]: string[] };
}

const KenBurnsImage: React.FC<{
  src: string;
  startFrame: number;
  durationInFrames: number;
  startScale?: number;
  endScale?: number;
  startX?: number;
  endX?: number;
  startY?: number;
  endY?: number;
}> = ({
  src,
  startFrame,
  durationInFrames,
  startScale = 1,
  endScale = 1.15,
  startX = 50,
  endX = 50,
  startY = 40,
  endY = 40,
}) => {
  const frame = useCurrentFrame();
  const localFrame = Math.max(0, frame - startFrame);
  const safeDuration = Math.max(1, durationInFrames);

  const scale = interpolate(localFrame, [0, safeDuration], [startScale, endScale], {
    extrapolateRight: "clamp",
  });
  const x = interpolate(localFrame, [0, safeDuration], [startX, endX], {
    extrapolateRight: "clamp",
  });
  const y = interpolate(localFrame, [0, safeDuration], [startY, endY], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile(src)}
        style={{
          position: "absolute",
          width: "115%",
          height: "115%",
          top: "-7.5%",
          left: "-7.5%",
          objectFit: "cover",
          transform: `scale(${scale})`,
          transformOrigin: `${x}% ${y}%`,
        }}
      />
    </div>
  );
};

const Documentary: React.FC<VideoProps> = ({
  audioPath,
  scenes,
  posts,
  profileScreenshot,
  profileName,
  handle,
  duration,
  relatedPostsByScene,
  focusPointsByScene = {},
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: "#020617" }}>
      {audioPath && <Audio src={staticFile("narration.mp3")} />}

      {scenes.map((scene) => {
        const startFrame = Math.floor(scene.start * fps);
        const endFrame = Math.floor(scene.end * fps);
        const sceneDuration = Math.max(1, endFrame - startFrame);

        if (frame < startFrame - fps || frame > endFrame + fps) {
          return null;
        }

        const fadeIn = interpolate(
          frame,
          [startFrame - fps * 0.5, startFrame + fps * 0.5],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );
        const fadeOut = interpolate(
          frame,
          [endFrame - fps * 0.5, endFrame + fps * 0.5],
          [1, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );
        const sceneOpacity = Math.min(fadeIn, fadeOut);

        const relatedPosts = (relatedPostsByScene[scene.sceneId] || [])
          .map((idx) => posts[idx])
          .filter(Boolean);

        const focusPoints = focusPointsByScene[scene.sceneId] || [];

        // If no posts, show profile for full duration
        if (relatedPosts.length === 0) {
           const screenshotSrc = profileScreenshot || "profile.png";
           // For profile shots, zoom differently (center-ish)
           const startY = 40;
           const endScale = 1.15;
           
           return (
             <AbsoluteFill
                key={scene.sceneId}
                style={{ opacity: sceneOpacity, position: "absolute", inset: 0 }}
             >
                <KenBurnsImage
                  src={screenshotSrc}
                  startFrame={startFrame}
                  durationInFrames={sceneDuration}
                  startScale={1}
                  endScale={endScale}
                  startX={50}
                  endX={50}
                  startY={startY}
                  endY={startY}
                />
             </AbsoluteFill>
           );
        }

        // If posts exist, split the scene duration among them
        const segmentDuration = sceneDuration / relatedPosts.length;

        return (
          <AbsoluteFill key={scene.sceneId} style={{ opacity: sceneOpacity, position: "absolute", inset: 0 }}>
            {relatedPosts.map((post, index) => {
               const segmentStart = startFrame + (index * segmentDuration);
               // Ensure the last segment goes exactly to endFrame to avoid gaps
               const segmentEnd = index === relatedPosts.length - 1 ? endFrame : segmentStart + segmentDuration;
               
               // Only render if within relevant window (plus fade margin)
               if (frame < segmentStart - fps || frame > segmentEnd + fps) return null;

               const isPostScreenshot = !!post.screenshotPath;
               const screenshotSrc = post.screenshotPath || profileScreenshot || "profile.png";

               let startScale = 1;
               let endScale = 1.25;
               let startX = 50;
               let startY = 30; 

               if (!isPostScreenshot) {
                 startY = 40;
                 endScale = 1.15;
               }

               if (focusPoints.length > 0 && isPostScreenshot) {
                 endScale = 1.6;
                 if (focusPoints.some(p => p.toLowerCase().includes("reply") || p.toLowerCase().includes("engagement"))) {
                   startY = 70;
                 }
               }
               
               // Crossfade between internal segments
               // We need local opacity for the sub-segment transition
               // But the outer sceneOpacity handles the scene edges.
               // We only need to handle the transition between Post A and Post B.
               
               const segmentFadeIn = index === 0 ? 1 : interpolate(
                 frame,
                 [segmentStart, segmentStart + fps * 0.5],
                 [0, 1],
                 { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
               );
               
               const segmentFadeOut = index === relatedPosts.length - 1 ? 1 : interpolate(
                 frame,
                 [segmentEnd - fps * 0.5, segmentEnd],
                 [1, 0],
                 { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
               );

               const segmentOpacity = Math.min(segmentFadeIn, segmentFadeOut);

               return (
                  <AbsoluteFill
                    key={`${scene.sceneId}_post_${index}`}
                    style={{ opacity: segmentOpacity }}
                  >
                    <KenBurnsImage
                      src={screenshotSrc}
                      startFrame={Math.floor(segmentStart)}
                      durationInFrames={Math.floor(segmentEnd - segmentStart)}
                      startScale={startScale}
                      endScale={endScale}
                      startX={startX}
                      endX={startX}
                      startY={startY}
                      endY={startY}
                    />
                  </AbsoluteFill>
               );
            })}
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};

export const TweetscapeDoc: React.FC = () => {
  return (
    <>
      <Composition
        id="TweetscapeDoc"
        component={Documentary}
        fps={30}
        width={1920}
        height={1080}
        durationInFrames={1}
        defaultProps={{
          audioPath: "",
          scenes: [],
          posts: [],
          profileScreenshot: "",
          profileName: "Unknown",
          handle: "unknown",
          duration: 60,
          relatedPostsByScene: {},
          focusPointsByScene: {},
        }}
        calculateMetadata={async ({ props }) => {
          const fps = 30;
          const durationInFrames = Math.ceil(props.duration * fps) + fps * 3;
          return { durationInFrames };
        }}
      />
    </>
  );
};

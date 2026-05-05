import { Layers, ArrowRight, Lightbulb, Network } from "lucide-react";

export default function ExplainerPage() {
  const sections = [
    {
      title: "What this is",
      body: "Replace this copy with a concise framing of the topic. Keep it short, concrete, and practical.",
    },
    {
      title: "How it works",
      body: "Describe the mechanism in steps. Use language a smart non-specialist can follow.",
    },
    {
      title: "Why it matters",
      body: "End with impact. What decisions change after understanding this?",
    },
  ];

  return (
    <div
      className="min-h-screen text-zinc-100"
      style={{
        background:
          "radial-gradient(1200px 600px at 10% -10%, rgba(56,189,248,0.18), transparent 55%), radial-gradient(1000px 500px at 100% 10%, rgba(167,139,250,0.16), transparent 52%), #0a0a0f",
      }}
    >
      <main className="mx-auto w-full max-w-6xl px-5 py-12 md:px-8 md:py-16">
        <header className="mb-10 rounded-3xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur md:p-10">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-300/30 bg-cyan-300/10 px-3 py-1 text-xs font-semibold tracking-wide text-cyan-200">
            <Lightbulb className="h-3.5 w-3.5" />
            Visual Explainer
          </div>
          <h1 className="text-balance text-3xl font-semibold leading-tight md:text-5xl">
            Replace with your explainer title
          </h1>
          <p className="mt-4 max-w-3xl text-sm text-zinc-300 md:text-base">
            Replace with an executive summary that tells readers exactly what they will understand by the end.
          </p>
        </header>

        <section className="mb-10 grid gap-4 md:grid-cols-3">
          {sections.map((section, i) => (
            <article
              key={section.title}
              className="rounded-2xl border border-white/10 bg-white/[0.03] p-5"
            >
              <div className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-lg border border-violet-300/30 bg-violet-300/10 text-violet-200">
                {i === 0 ? <Layers className="h-4 w-4" /> : i === 1 ? <Network className="h-4 w-4" /> : <ArrowRight className="h-4 w-4" />}
              </div>
              <h2 className="text-lg font-medium">{section.title}</h2>
              <p className="mt-2 text-sm leading-relaxed text-zinc-300">{section.body}</p>
            </article>
          ))}
        </section>

        <section className="rounded-3xl border border-white/10 bg-gradient-to-b from-white/[0.06] to-white/[0.02] p-6 md:p-8">
          <h2 className="text-xl font-semibold md:text-2xl">System map</h2>
          <p className="mt-2 text-sm text-zinc-300 md:text-base">
            Swap this placeholder with a real architecture flow, timeline, comparison matrix, or process map tailored to the topic.
          </p>
          <div className="mt-6 grid gap-3 md:grid-cols-3">
            <div className="rounded-xl border border-cyan-200/20 bg-cyan-500/10 p-4 text-sm text-cyan-100">Input</div>
            <div className="rounded-xl border border-fuchsia-200/20 bg-fuchsia-500/10 p-4 text-sm text-fuchsia-100">Transformation</div>
            <div className="rounded-xl border border-emerald-200/20 bg-emerald-500/10 p-4 text-sm text-emerald-100">Output</div>
          </div>
        </section>
      </main>
    </div>
  );
}

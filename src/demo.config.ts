import type { DemoConfig } from './types'

const technicalTopology = {
  boundary: { label: 'OpenShift namespace', detail: 'application deployment boundary' },
  entry: { id: 'browser', kind: 'operator', label: 'Presenter browser', detail: 'story + live workspace' },
  primaryPath: [
    { id: 'route', kind: 'route', label: 'Route / ingress', detail: 'TLS edge and public entry', endpoint: '443', edgeLabel: 'HTTPS' },
    { id: 'service', kind: 'service', label: 'Application Service', detail: 'stable cluster endpoint', endpoint: ':8080', edgeLabel: 'HTTP' },
    { id: 'runtime', kind: 'deployment', label: 'Application runtime', detail: 'UI, API, and orchestration', endpoint: 'POST /api/proof', edgeLabel: 'selects pod' },
    { id: 'proof-service', kind: 'service', label: 'Proof Service', detail: 'bounded internal endpoint', endpoint: ':8090', edgeLabel: 'typed API' },
  ],
  supportPath: [
    { id: 'evidence', kind: 'data', label: 'Approved evidence', detail: 'versioned fixtures or live source', edgeLabel: 'retrieval' },
    { id: 'policy', kind: 'policy', label: 'Decision policy', detail: 'validate, compare, or abstain', edgeLabel: 'evaluate' },
    { id: 'human', kind: 'authority', label: 'Human decision', detail: 'authority remains visible', edgeLabel: 'proposal' },
  ],
  optionalPath: { id: 'optional', kind: 'external', label: 'Optional integration', detail: 'never implied to be authoritative', edgeLabel: 'bounded egress' },
}

export const demoConfig: DemoConfig = {
  id: 'virtualization-ai-201', title: "Build and Qualify a VM-to-AI Contract", subtitle: "Red Hat × Intel Virtualization + AI 201", event: 'Customer briefing', audience: 'Enterprise technology leaders', cta: 'Choose the depth that fits the room.',
  brand: { primary: { name: 'Red Hat', logo: '/logos/redhat.svg', alt: 'Red Hat' }, partner: { name: 'Intel', logo: '/logos/intel.png', alt: 'Intel' }, attribution: 'Red Hat × Intel' },
  acts: [
    { id: 'story', label: '00', title: 'The Decision', scenes: [
      { id: 'intro', type: 'intro', beat: 'ordinary-world', title: 'Build the proof, not just the pitch', subtitle: 'A reusable Red Hat × Intel live-demo journey', speakerPrompt: 'Start with the audience reality and the decision they need to make—not the component inventory.' },
      { id: 'reframe', type: 'reframe', beat: 'stakes', eyebrow: 'The tension', title: 'A feature tour cannot earn the decision', before: 'Describe every capability', after: 'Make one claim observable', detail: 'The short story frames the tension. Architecture, proof, and guided practice each have a separate job.', speakerPrompt: 'Name the risk of the status quo, then state the new decision in one sentence.' },
    ] },
    { id: 'architecture', label: '01', title: 'Guided Architecture', scenes: [
      { id: 'guided-architecture', type: 'guided-architecture', beat: 'system-reveal', eyebrow: 'Guided architecture', title: 'Reveal only what the audience needs to believe', body: 'Each question earns one component, responsibility, and boundary.', layers: [
        { id: 'input', component: 'Experience input', tone: 'primary', question: 'What enters the system?', answer: 'A bounded, validated request starts the journey.', detail: 'Show the contract, source, and assumptions before discussing implementation.', activeNodeIds: ['browser', 'route'] },
        { id: 'platform', component: 'Red Hat platform', tone: 'primary', question: 'Where does the workload run and remain governable?', answer: 'The platform owns deployment, policy, isolation, and operations.', detail: 'Include only platform services that alter proof, risk, or the audience decision.', activeNodeIds: ['service', 'runtime'] },
        { id: 'compute', component: 'Intel compute', tone: 'partner', question: 'What makes the workload practical here?', answer: 'The selected compute path supports the workload claim.', detail: 'Use measured evidence for performance, placement, or efficiency claims.', activeNodeIds: ['proof-service'] },
        { id: 'proof', component: 'Proof adapter', tone: 'success', question: 'How will the audience know the claim is true?', answer: 'A typed adapter returns observable evidence and source state.', detail: 'Live, rehearsal, and offline results are labeled honestly and retain timestamps.', activeNodeIds: ['evidence', 'policy'] },
        { id: 'decision', component: 'Human decision', tone: 'primary', question: 'Who decides what happens next?', answer: 'The audience reviews the evidence and chooses the next journey.', detail: 'End architecture at the human outcome, not at the final technology box.', activeNodeIds: ['human'] },
      ], technicalTopology, speakerPrompt: 'Pause on every question. Invite an answer, then reveal the actual runtime objects and boundary before advancing.' },
    ] },
    { id: 'proof', label: '02', title: 'Live Walkthrough', scenes: [
      { id: 'live', type: 'live-journey', beat: 'live-proof', eyebrow: 'Live infrastructure · guided walkthrough', title: 'Watch evidence move through the architecture', body: 'Run one condition, pause on its evidence, then change the input and prove that the system responds.', cta: 'Run the live journey', workspace: { label: 'Open the live workspace', href: '/' }, nodes: [
        { id: 'input', label: 'Experience input', detail: 'bounded request', tone: 'primary' },
        { id: 'platform', label: 'Red Hat platform', detail: 'policy and operations', tone: 'primary' },
        { id: 'compute', label: 'Intel compute', detail: 'measured execution', tone: 'partner' },
        { id: 'adapter', label: 'Proof adapter', detail: 'typed evidence', tone: 'success' },
        { id: 'decision', label: 'Human decision', detail: 'authority stays visible', tone: 'primary' },
      ], technicalTopology, steps: [
        { id: 'baseline', title: 'Run the first condition', detail: 'The live response activates the system path and exposes its source state.', adapterId: 'demo-proof', activeNode: 3, activeNodeIds: ['browser', 'route', 'service', 'runtime', 'proof-service', 'evidence', 'policy'], resultFields: [{ key: 'latency', label: 'Latency', suffix: 'ms' }, { key: 'throughput', label: 'Throughput', suffix: '/s' }, { key: 'outcome', label: 'Outcome' }] },
        { id: 'changed', title: 'Change the evidence', detail: 'A second condition must produce a distinguishable result through the same architecture.', adapterId: 'demo-proof-changed', activeNode: 4, activeNodeIds: ['browser', 'route', 'service', 'runtime', 'proof-service', 'evidence', 'policy', 'human'], resultFields: [{ key: 'latency', label: 'Latency', suffix: 'ms' }, { key: 'throughput', label: 'Throughput', suffix: '/s' }, { key: 'outcome', label: 'Outcome' }] },
      ], speakerPrompt: 'Narrate the deployment objects, protocols, trust boundary, and active path while it runs. Say LIVE, REHEARSAL, or OFFLINE before interpreting each result.' },
      { id: 'tradeoff', type: 'comparison', beat: 'trials', title: 'Show the decision boundary, not only the winner', columns: [{ label: 'Claim', value: 'Observable', detail: 'The proof answers the question posed by the story.', tone: 'success' }, { label: 'Limit', value: 'Explicit', detail: 'Scope, fallback state, and next validation remain visible.', tone: 'partner' }], speakerPrompt: 'Stop adding slides. Use the limitation to choose the next live or guided depth.' },
    ] },
    { id: 'mechanisms', label: '03', title: 'Why It Works', scenes: [
      { id: 'mechanisms', type: 'mechanisms', beat: 'trials', eyebrow: 'Why it worked', title: 'Expose the few mechanisms that make the result repeatable', body: 'Each card explains why the proof behaved as it did before the audience enters the lab.', mechanisms: [
        { id: 'placement', label: 'Measured placement', claim: 'Route work by evidence, not assumption.', detail: 'The same request contract can select a different execution path when the condition changes.', tone: 'partner' },
        { id: 'policy', label: 'Visible policy', claim: 'Keep the decision boundary inspectable.', detail: 'Operators can see the rule, evidence, and limitation that shaped the result.', tone: 'primary' },
        { id: 'fallback', label: 'Honest resilience', claim: 'Degrade without disguising the source.', detail: 'Rehearsal and offline evidence remain useful while visibly distinct from a live response.', tone: 'success' },
      ], speakerPrompt: 'Explain only the mechanisms needed to make the observed result understandable and repeatable.' },
    ] },
    { id: 'payoff', label: '04', title: 'Evidence & Handoff', scenes: [
      { id: 'payoff', type: 'evidence-payoff', beat: 'transformation', eyebrow: 'What you just proved', title: 'Close with evidence from this session', adapterIds: ['demo-proof', 'demo-proof-changed'], fallbackLine: 'Run the live journey to populate this payoff', evidenceFields: [{ key: 'latency', label: 'Latest latency', suffix: 'ms' }, { key: 'throughput', label: 'Latest throughput', suffix: '/s' }, { key: 'outcome', label: 'Observed outcome' }], line1: 'The architecture did not end at the diagram.', line2: 'It produced evidence the room can inspect.', cta: 'Continue into guided practice or the lab →', speakerPrompt: 'Recap only evidence produced in this session. If proof was not run, say so and return to the live act.' },
    ] },
  ],
  journeyHandoffs: [
    { depth: 'guided', title: 'Guided experience', duration: '20–35 minutes', question: 'Can the audience trace and challenge the evidence?', technology: 'Live workspace · Guided inspection · Human decision', instruction: 'Continue the same evidence path with participant decisions.', href: '/' },
  ],
}

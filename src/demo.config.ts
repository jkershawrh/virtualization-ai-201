import type { DemoConfig } from './types'

const technicalTopology = {
  boundary: { label: 'OpenShift participant namespace', detail: 'learner-authored contract boundary' },
  entry: { id: 'vm-client', kind: 'VirtualMachine client', label: 'VM contract client', detail: 'creates correlation ID, guest identity, and request hash', endpoint: 'guest Python' },
  primaryPath: [
    { id: 'service', kind: 'v1 Service', label: 'qualification adapter', detail: 'stable namespace-local endpoint', endpoint: ':8080', edgeLabel: 'HTTP JSON' },
    { id: 'adapter', kind: 'apps/v1 Deployment', label: 'validation adapter', detail: 'schema, secret boundary, output validation, evidence', endpoint: 'POST /api/v1/qualify', edgeLabel: 'selects pod' },
    { id: 'model', kind: 'governed inference', label: 'Intel Xeon model endpoint', detail: 'bounded advisory interpretation only', endpoint: 'OpenAI-compatible HTTPS', edgeLabel: 'conditional egress' },
  ],
  supportPath: [
    { id: 'secret', kind: 'Secret reference', label: 'Runtime identity', detail: 'endpoint, model, provider, hardware, API key; never in the VM', edgeLabel: 'secretKeyRef' },
    { id: 'evidence', kind: 'evidence API', label: 'Qualification record', detail: 'request hash, path, source state, validation, failure', endpoint: 'GET /api/v1/evidence/{id}', edgeLabel: 'correlate' },
    { id: 'human', kind: 'authority', label: 'Human reviewer', detail: 'accepts or rejects the learner bundle', edgeLabel: 'review' },
  ],
  optionalPath: { id: 'policy', kind: 'NetworkPolicy', label: 'Declared path only', detail: 'VM and presentation ingress; DNS plus approved model egress', edgeLabel: 'allow list' },
}

export const demoConfig: DemoConfig = {
  id: 'virtualization-ai-201',
  title: 'Virtualization + AI 201',
  subtitle: 'Build and qualify a VM-to-AI contract',
  event: 'Red Hat × Intel technical briefing',
  audience: 'Application and platform engineers who can already trace the 101 path',
  cta: 'Author the boundary. Break it safely. Keep approval human.',
  brand: {
    primary: { name: 'Red Hat', logo: '/logos/redhat.svg', alt: 'Red Hat' },
    partner: { name: 'Intel', logo: '/logos/intel.png', alt: 'Intel' },
    attribution: 'Red Hat × Intel',
  },
  acts: [
    {
      id: 'decision', label: '00', title: 'The Decision', scenes: [
        {
          id: 'intro', type: 'intro', beat: 'ordinary-world',
          title: 'A model can be reachable while the integration remains unqualified.',
          subtitle: '201 begins after the 101 trace: the learner must author every boundary.',
          speakerPrompt: 'State the prerequisite plainly. The 101 evidence is upstream context, not proof that this learner built the contract.',
        },
        {
          id: 'reframe', type: 'reframe', beat: 'stakes', eyebrow: 'The reframe',
          title: 'The deliverable is not a successful prompt',
          before: 'A VM sends JSON and receives text',
          after: 'A human can defend the complete contract bundle',
          detail: 'Schemas, guest identity, Secret reference, Service, NetworkPolicy, validation, failure, evidence, authority, and cleanup must agree.',
          speakerPrompt: 'A happy-path curl hides the decisions. Ask which boundary rejects an incompatible request, protects the credential, and prevents an invented answer.',
        },
      ],
    },
    {
      id: 'architecture', label: '01', title: 'Causal Architecture', scenes: [
        {
          id: 'guided-architecture', type: 'guided-architecture', beat: 'system-reveal', eyebrow: 'Learner-authored boundaries',
          title: 'Each artifact answers one qualification question',
          body: 'Reveal the contract in the same order the learner must construct and defend it.',
          layers: [
            { id: 'request', component: 'Request schema + VM client', tone: 'primary', question: 'What may leave the guest?', answer: 'A versioned, bounded request with guest and correlation identity.', detail: 'The client emits a request hash and has no path to a model credential.', activeNodeIds: ['vm-client'] },
            { id: 'network', component: 'Service + NetworkPolicy', tone: 'primary', question: 'Which network path is intentionally open?', answer: 'The namespace Service selects the adapter; policy admits only declared clients.', detail: 'DNS is allowed. Model HTTPS egress exists only for an approved CIDR.', activeNodeIds: ['vm-client', 'service', 'policy'] },
            { id: 'credential', component: 'Secret reference + adapter', tone: 'success', question: 'Where does model identity enter?', answer: 'The adapter reads the runtime Secret by reference and validates before inference.', detail: 'No secret value appears in the VM, browser, fixture, evidence, or repository.', activeNodeIds: ['vm-client', 'service', 'adapter', 'secret', 'policy'] },
            { id: 'failure', component: 'Response contract + evidence', tone: 'partner', question: 'What happens when the model cannot answer?', answer: 'The same contract returns a typed unavailable result and no advisory fields.', detail: 'Correlation and human authority survive; fabricated model output does not.', activeNodeIds: ['vm-client', 'service', 'adapter', 'evidence', 'policy'] },
            { id: 'authority', component: 'Human reviewer', tone: 'primary', question: 'Who qualifies the integration?', answer: 'The reviewer accepts or rejects the evidence bundle.', detail: 'The model has no tools, mutation path, self-approval, certification, or promotion authority.', activeNodeIds: ['vm-client', 'service', 'adapter', 'model', 'secret', 'evidence', 'human', 'policy'] },
          ],
          technicalTopology,
          speakerPrompt: 'Ask and pause before each reveal. Keep learner work, platform enforcement, model participation, and human authority visually distinct.',
        },
      ],
    },
    {
      id: 'proof', label: '02', title: 'Qualification Proof', scenes: [
        {
          id: 'live-journey', type: 'live-journey', beat: 'live-proof', eyebrow: 'Same contract · two conditions',
          title: 'Healthy evidence is incomplete until failure is qualified',
          body: 'Run the authored request, preserve its evidence, then change only model availability.',
          cta: 'Run the qualification journey',
          nodes: [
            { id: 'vm-client', label: 'VM client', detail: 'authored request', tone: 'primary' },
            { id: 'service', label: 'Service + policy', detail: 'declared path', tone: 'primary' },
            { id: 'adapter', label: 'Validation adapter', detail: 'contract + secret', tone: 'success' },
            { id: 'model', label: 'Xeon model', detail: 'advisory only', tone: 'partner' },
            { id: 'human', label: 'Human reviewer', detail: 'final authority', tone: 'primary' },
          ],
          technicalTopology,
          steps: [
            {
              id: 'qualified', title: 'Qualify the healthy path', detail: 'A valid request returns explicit source state, validation, evidence identity, and human authority.',
              adapterId: 'qualification-healthy', activeNode: 4,
              activeNodeIds: ['vm-client', 'service', 'adapter', 'model', 'secret', 'evidence', 'human', 'policy'],
              resultFields: [
                { key: 'source_state', label: 'Source state' }, { key: 'outcome', label: 'Outcome' },
                { key: 'ai_participated', label: 'AI participated' }, { key: 'model_id', label: 'Model' },
                { key: 'category', label: 'Category' }, { key: 'authority', label: 'Authority' },
              ],
            },
            {
              id: 'unavailable', title: 'Qualify model unavailability', detail: 'The same schema and path preserve correlation while omitting every advisory and model claim.',
              adapterId: 'qualification-unavailable', activeNode: 4,
              activeNodeIds: ['vm-client', 'service', 'adapter', 'evidence', 'human', 'policy'],
              resultFields: [
                { key: 'source_state', label: 'Source state' }, { key: 'outcome', label: 'Outcome' },
                { key: 'ai_participated', label: 'AI participated' }, { key: 'model_id', label: 'Model' },
                { key: 'category', label: 'Category' }, { key: 'authority', label: 'Authority' },
              ],
            },
          ],
          speakerPrompt: 'Say LIVE, REHEARSAL, or OFFLINE before interpreting either result. Keep the first result visible; qualification depends on the contrast.',
        },
        {
          id: 'decision-boundary', type: 'comparison', beat: 'trials',
          title: 'The unavailable path tests whether the contract tells the truth',
          columns: [
            { label: 'Qualified condition', value: 'Bounded advisory', detail: 'Identity and validation support human review; they do not grant action authority.', tone: 'success' },
            { label: 'Unavailable condition', value: 'No invented answer', detail: 'Failure remains attributable and contains no advisory, model, or live-AI claim.', tone: 'partner' },
          ],
          speakerPrompt: 'No quantitative claim is needed. The evidence is whether the contract changes only the fields it is allowed to change.',
        },
      ],
    },
    {
      id: 'mechanism', label: '03', title: 'Why It Holds', scenes: [
        {
          id: 'mechanisms', type: 'mechanisms', beat: 'trials', eyebrow: 'CDD → TDD → EDD',
          title: 'Three disciplines make the learner work reviewable',
          mechanisms: [
            { id: 'cdd', label: 'Contract-driven', claim: 'The acceptance boundary exists before implementation.', detail: 'The retained RED run proves schemas and tests preceded the adapter, client, and manifests.', tone: 'primary' },
            { id: 'tdd', label: 'Test-driven', claim: 'Healthy, rejected, and unavailable paths share executable checks.', detail: 'Secret-bearing input, incomplete live identity, and fabricated unavailable output fail closed.', tone: 'partner' },
            { id: 'edd', label: 'Evidence-driven', claim: 'Every accepted claim maps to a redacted record.', detail: 'Correlation joins guest, Service, model state, validation, authority, and cleanup without retaining the raw note.', tone: 'success' },
          ],
          speakerPrompt: 'The lab is construction depth. Learners edit starter artifacts, run the gates, invoke the VM, compare failure, and reclaim the namespace.',
        },
      ],
    },
    {
      id: 'payoff', label: '04', title: 'Evidence & Handoff', scenes: [
        {
          id: 'payoff', type: 'evidence-payoff', beat: 'transformation', eyebrow: 'What this session proved',
          title: 'A contract is qualified only when a human can explain its limits',
          adapterIds: ['qualification-healthy', 'qualification-unavailable'],
          fallbackLine: 'Run both conditions to populate the current-session evidence',
          evidenceFields: [
            { key: 'source_state', label: 'Latest source state' }, { key: 'outcome', label: 'Latest outcome' },
            { key: 'ai_participated', label: 'AI participated' }, { key: 'authority', label: 'Final authority' },
          ],
          line1: 'The learner authored the boundary, not merely the prompt.',
          line2: 'Certification still belongs to Launchpad.',
          cta: 'Close presentation, then begin the 75–90 minute Showroom lab →',
          speakerPrompt: 'Recap only current-session evidence. State that no live OpenShift, capacity, reclaim certification, or promotion result exists in factory mode.',
        },
      ],
    },
  ],
  journeyHandoffs: [
    {
      depth: 'lab', title: 'Virtualization + AI 201 hands-on lab', duration: '75–90 minutes',
      question: 'Can the learner author, break, qualify, explain, and reclaim the contract?',
      technology: 'OpenShift Virtualization · Service · NetworkPolicy · Secret reference · Intel Xeon inference · Showroom',
      instruction: 'Open the separate Showroom guide. Begin in lab/starter; 101 receipts are prerequisite context, not completion evidence.',
    },
  ],
}

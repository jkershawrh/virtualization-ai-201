import { registerAdapter } from './adapters'
import qualifiedFixture from './fixtures/qualified.json'
import unavailableFixture from './fixtures/unavailable.json'
import type { LiveDataAdapter } from '../types'

type FlatResult = Record<string, unknown> & {
  source_state: string
  outcome: string
  ai_participated: string
  model_id: string
  category: string
  authority: string
  evidence_id: string
}

type QualificationResponse = {
  correlation_id: string
  outcome: 'QUALIFIED' | 'MODEL_UNAVAILABLE'
  source_state: 'LIVE' | 'REHEARSAL' | 'OFFLINE'
  ai_participated: boolean
  advisory?: { category: string; summary: string; rationale: string }
  model?: { id: string; provider: string; hardware: string }
  validation: 'PASS' | 'FAIL_CLOSED'
  authority: 'HUMAN_REVIEW_REQUIRED'
  evidence_id: string
}

function flatten(response: QualificationResponse): FlatResult {
  return {
    source_state: response.source_state,
    outcome: response.outcome,
    ai_participated: response.ai_participated ? 'yes' : 'no',
    model_id: response.model?.id ?? 'none',
    category: response.advisory?.category ?? 'none',
    authority: response.authority,
    evidence_id: response.evidence_id,
  }
}

function qualificationAdapter(id: string, unavailable: boolean, fixture: FlatResult): LiveDataAdapter<FlatResult> {
  return {
    id,
    timeoutMs: 3_000,
    rehearsal: { data: fixture, collectedAt: '2026-09-28T20:00:00.000Z' },
    async load(signal) {
      const correlationId = crypto.randomUUID()
      const response = await fetch(`/api/v1/qualify${unavailable ? '?condition=unavailable' : ''}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          schema_version: 'virtualization-ai.redhat-intel.com/qualification-request/v1',
          correlation_id: correlationId,
          guest: { name: 'contract-author-vm', namespace: 'virtualization-ai-201' },
          task: 'classify-operations-note',
          note: 'The application resolves the Service, then stops at the model boundary.',
          allowed_categories: ['application', 'capacity', 'connectivity', 'unknown'],
        }),
        signal,
      })
      if (!response.ok) throw new Error(`Qualification endpoint returned HTTP ${response.status}`)
      const data = await response.json() as QualificationResponse
      if (data.source_state !== 'LIVE') throw new Error(`Endpoint reported ${data.source_state}, not LIVE`)
      if (!unavailable && (!data.ai_participated || !data.model?.id || data.validation !== 'PASS')) {
        throw new Error('Healthy result did not establish live model identity and validation')
      }
      if (unavailable && (data.ai_participated || data.advisory || data.model || data.validation !== 'FAIL_CLOSED')) {
        throw new Error('Unavailable result did not fail closed')
      }
      return flatten(data)
    },
  }
}

registerAdapter(qualificationAdapter('qualification-healthy', false, qualifiedFixture))
registerAdapter(qualificationAdapter('qualification-unavailable', true, unavailableFixture))

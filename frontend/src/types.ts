export type Product = {
  id: string
  name: string
  brand: string
  price_usd: number
  summary: string
  specs: {
    ram_gb: number
    weight_lbs: number
    gpu: string
    battery_wh: number
  }
}

export type Citation = {
  source: string
  quote: string
  chunk_index: number
  score: number
}

export type ResearchResponse = {
  question: string
  top_pick: Product | null
  alternatives: Product[]
  why: string[]
  disadvantages: string[]
  missing_info: string[]
  citations: Citation[]
  steps: string[]
}

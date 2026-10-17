import { useState } from 'react'
import type { FormEvent } from 'react'
import { researchLaptops } from './api'
import type { Product, ResearchResponse } from './types'
import './App.css'

const EXAMPLES = [
  'best laptop under $1000 for programming',
  'lightweight laptop for travel and coding',
  'laptop for programming and occasional gaming',
]

function ProductCard({ product, label }: { product: Product; label?: string }) {
  return (
    <div className="product">
      {label ? <p className="label">{label}</p> : null}
      <h3>{product.name}</h3>
      <p className="meta">
        {product.brand} · ${product.price_usd} · {product.specs.ram_gb}GB RAM ·{' '}
        {product.specs.weight_lbs} lb
      </p>
      <p>{product.summary}</p>
    </div>
  )
}

export default function App() {
  const [question, setQuestion] = useState(EXAMPLES[0])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<ResearchResponse | null>(null)

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const data = await researchLaptops(question.trim())
      setResult(data)
    } catch (err) {
      setResult(null)
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <header>
        <p className="eyebrow">Scout AI</p>
        <h1>Laptop research assistant</h1>
        <p className="lede">
          Ask a buying question. The backend searches the catalog, retrieves
          cited notes, and returns a structured recommendation.
        </p>
      </header>

      <form onSubmit={onSubmit} className="ask">
        <label htmlFor="question">Your question</label>
        <textarea
          id="question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          required
        />
        <div className="examples">
          {EXAMPLES.map((example) => (
            <button
              key={example}
              type="button"
              className="chip"
              onClick={() => setQuestion(example)}
            >
              {example}
            </button>
          ))}
        </div>
        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? 'Researching…' : 'Research'}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {result ? (
        <section className="results">
          {result.top_pick ? (
            <ProductCard product={result.top_pick} label="Top pick" />
          ) : (
            <p>No matching product found.</p>
          )}

          {result.alternatives.length > 0 ? (
            <div>
              <h2>Alternatives</h2>
              {result.alternatives.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : null}

          <div>
            <h2>Why</h2>
            <ul>
              {result.why.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          <div>
            <h2>Disadvantages</h2>
            <ul>
              {result.disadvantages.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          <div>
            <h2>Missing info</h2>
            <ul>
              {result.missing_info.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          <div>
            <h2>Citations</h2>
            {result.citations.map((citation) => (
              <blockquote key={`${citation.source}-${citation.chunk_index}`}>
                <p>{citation.quote}</p>
                <footer>
                  {citation.source} · score {citation.score}
                </footer>
              </blockquote>
            ))}
          </div>

          <p className="steps">Steps: {result.steps.join(' → ')}</p>
        </section>
      ) : null}
    </main>
  )
}

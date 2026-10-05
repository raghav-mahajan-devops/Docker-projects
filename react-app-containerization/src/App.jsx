import { useEffect, useState } from 'react'

const STORAGE_KEY = 'docker-checklist'

const DEFAULT_TASKS = [
  { id: 1, text: 'Write a Dockerfile', done: true },
  { id: 2, text: 'Build the image', done: false },
  { id: 3, text: 'Run the container', done: false },
  { id: 4, text: 'Push the image to a registry', done: false },
]

export default function App() {
  const [tasks, setTasks] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      return saved ? JSON.parse(saved) : DEFAULT_TASKS
    } catch {
      return DEFAULT_TASKS
    }
  })
  const [text, setText] = useState('')

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks))
  }, [tasks])

  const add = (e) => {
    e.preventDefault()
    const value = text.trim()
    if (!value) return
    setTasks([...tasks, { id: Date.now(), text: value, done: false }])
    setText('')
  }

  const toggle = (id) =>
    setTasks(tasks.map((t) => (t.id === id ? { ...t, done: !t.done } : t)))

  const remove = (id) => setTasks(tasks.filter((t) => t.id !== id))

  const doneCount = tasks.filter((t) => t.done).length
  const percent = tasks.length ? Math.round((doneCount / tasks.length) * 100) : 0

  return (
    <main className="card">
      <header>
        <h1>Docker Checklist</h1>
        <p>A React app served from a Docker container.</p>
      </header>

      <div className="progress" aria-label={`${percent}% complete`}>
        <div className="bar" style={{ width: `${percent}%` }} />
      </div>
      <p className="count">
        {doneCount} of {tasks.length} done
      </p>

      <form onSubmit={add}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add a task"
          aria-label="New task"
        />
        <button type="submit">Add</button>
      </form>

      {tasks.length === 0 && <p className="empty">No tasks yet. Add one above.</p>}

      <ul>
        {tasks.map((t) => (
          <li key={t.id} className={t.done ? 'done' : ''}>
            <label>
              <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
              <span>{t.text}</span>
            </label>
            <button className="remove" onClick={() => remove(t.id)} aria-label={`Delete ${t.text}`}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </main>
  )
}

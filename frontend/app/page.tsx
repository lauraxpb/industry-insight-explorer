'use client';
import { useState } from 'react';

export default function Home() {
	const [query, setQuery] = useState('');
	const [industry, setIndustry] = useState<any>(null);
	const [insight, setInsight] = useState<string | null>(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [searched, setSearched] = useState(false);

	const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

	const searchIndustry = async () => {
		setLoading(true);
		setSearched(false);
		setInsight(null);
		setIndustry(null);

		const res = await fetch(`${API_URL}/search/industries?query=${query}`);

		const data = await res.json();
		setIndustry(data[0] || null);
		setSearched(true);
		setLoading(false);
	};

	const generateInsight = async () => {
		if (!industry) return;

		setLoading(true);

		const res = await fetch(`${API_URL}/industries/${industry.slug}/insight`, {
			method: 'POST',
		});

		const data = await res.json();
		setInsight(data.content);
		setLoading(false);
	};

	return (
		<main style={{ padding: 40, fontFamily: 'system-ui' }}>
			<h1>Industry Insight Explorer</h1>

			<input
				placeholder="Ask something about an industry..."
				value={query}
				onChange={(event) => setQuery(event.target.value)}
				style={{ padding: 8, width: 300 }}
			/>

			<br />
			<br />

			<button onClick={searchIndustry} disabled={loading}>
				Discover
			</button>

			{searched && !loading && !industry && (
				<p>No industries found for that query.</p>
			)}

			{industry && (
				<>
					<h2>Detected Industry</h2>
					<p>
						<strong>{industry.name}</strong>
					</p>

					<button onClick={generateInsight} disabled={loading}>
						Generate Insight
					</button>
				</>
			)}

			{insight && (
				<>
					<h2>Insight</h2>
					<p>{insight}</p>
				</>
			)}
		</main>
	);
}

import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-black">
      <div className="mx-auto max-w-4xl px-6 py-16">
        <h1 className="text-4xl font-semibold tracking-tight">
          Multimodal RAG Demo
        </h1>
        <p className="mt-4 text-lg text-gray-600">
          Upload PDFs, tables, and images. Ask questions. Get answers with citations.
        </p>

        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border p-6 shadow-sm">
            <div className="text-sm font-medium text-gray-500">Step 1</div>
            <div className="mt-2 text-xl font-semibold">Upload documents</div>
            <p className="mt-2 text-gray-600">
              PDFs, CSV/XLSX tables, and images (captioned for retrieval).
            </p>
          </div>

          <div className="rounded-2xl border p-6 shadow-sm">
            <div className="text-sm font-medium text-gray-500">Step 2</div>
            <div className="mt-2 text-xl font-semibold">Chat with your docs</div>
            <p className="mt-2 text-gray-600">
              RAG pipeline retrieves relevant chunks and cites sources.
            </p>
          </div>
        </div>

        <div className="mt-12 flex gap-3">
          <a
            className="rounded-xl bg-black px-5 py-3 text-white hover:opacity-90"
            href="/upload"
          >
            Go to Upload
          </a>
          <a
            className="rounded-xl border px-5 py-3 hover:bg-gray-50"
            href="/chat"
          >
            Go to Chat
          </a>
        </div>

        <p className="mt-10 text-sm text-gray-500">
          (UI routes will be wired next — this is a scaffold.)
        </p>
      </div>
    </main>
  );
}

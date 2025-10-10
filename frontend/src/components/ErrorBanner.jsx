export default function ErrorBanner({ message }) {
  if (!message) return null;
  return (
    <div className="bg-red-600/20 border border-red-600/40 text-red-200 px-4 py-3 rounded mb-6">
      {message}
    </div>
  );
}

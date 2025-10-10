export default function Loader({ text = "Chargement..." }) {
  return (
    <div className="flex items-center justify-center py-10">
      <div className="animate-spin inline-block w-6 h-6 border-[3px] border-current border-t-transparent text-red-500 rounded-full mr-3" />
      <span className="text-gray-300">{text}</span>
    </div>
  );
}

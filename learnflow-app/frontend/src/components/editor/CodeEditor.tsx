"use client";

import dynamic from "next/dynamic";
import { useEditorStore } from "@/stores/editorStore";
import { Loading } from "@/components/ui/Loading";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => <Loading text="Loading editor..." className="h-96" />,
});

interface CodeEditorProps {
  height?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
  readOnly?: boolean;
}

export function CodeEditor({ height = "400px", defaultValue, onChange, readOnly = false }: CodeEditorProps) {
  const { code, setCode } = useEditorStore();
  const value = defaultValue !== undefined ? defaultValue : code;

  const handleChange = (val: string | undefined) => {
    const newValue = val || "";
    if (onChange) onChange(newValue);
    else setCode(newValue);
  };

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden">
      <MonacoEditor
        height={height} language="python" theme="vs-light"
        value={value} onChange={handleChange}
        options={{ minimap: { enabled: true }, fontSize: 14, lineNumbers: "on", scrollBeyondLastLine: false, automaticLayout: true, tabSize: 4, readOnly, wordWrap: "on" }}
      />
    </div>
  );
}

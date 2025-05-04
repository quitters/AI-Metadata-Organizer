'use client';
import React, { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import MetadataTable, { Metadata } from "./components/MetadataTable";

export default function Home() {
  const [metadata, setMetadata] = useState<Metadata[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelected = async (file: File) => {
    setLoading(true);
    setError(null);
    setMetadata([]);
    try {
      const formData = new FormData();
      formData.append("image", file);
      // Placeholder: API endpoint will be implemented later
      const response = await fetch("http://localhost:8000/api/extract-metadata", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Failed to extract metadata");
      const data = await response.json();
      setMetadata([data]);
    } catch (err: unknown) {
      if (typeof err === "object" && err !== null && "message" in err && typeof (err as any).message === "string") {
        setError((err as any).message);
      } else {
        setError("Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", padding: 32 }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 16 }}>AI Image Manager Web</h1>
      <ImageUpload onImageSelected={handleImageSelected} />
      {loading && <div style={{ marginTop: 24 }}>Extracting metadata...</div>}
      {error && <div style={{ color: "red", marginTop: 24 }}>{error}</div>}
      <MetadataTable data={metadata} />
    </div>
  );
}

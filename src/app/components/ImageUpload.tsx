'use client';
import React, { useRef } from "react";

interface ImageUploadProps {
  onImageSelected: (file: File) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onImageSelected }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      onImageSelected(event.target.files[0]);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      onImageSelected(event.dataTransfer.files[0]);
    }
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      style={{ border: "2px dashed #aaa", padding: 32, textAlign: "center", borderRadius: 12 }}
    >
      <p>Drag and drop a PNG image here, or</p>
      <button onClick={() => fileInputRef.current?.click()} style={{ margin: 8 }}>
        Select Image
      </button>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/png"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
    </div>
  );
};

export default ImageUpload;

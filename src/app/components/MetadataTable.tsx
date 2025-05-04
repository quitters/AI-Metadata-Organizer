import React from "react";
import styles from "./MetadataTable.module.css";

export interface Metadata {
  prompt: string;
  width: number;
  height: number;
  version?: string;
  profile?: string;
  job_id?: string;
  created_date?: string;
  author?: string;
  source_model?: string;
}

interface MetadataTableProps {
  data: Metadata[];
}

const MetadataTable: React.FC<MetadataTableProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>No metadata to display.</div>;
  }
  return (
    <table className={styles["metadata-table"]}>
      <thead>
        <tr>
          <th>Prompt</th>
          <th>Width</th>
          <th>Height</th>
          <th>Origin</th>
          <th>Version</th>
          <th>Profile</th>
          <th>Job ID</th>
          <th>Date</th>
          <th>Author</th>
        </tr>
      </thead>
      <tbody>
        {data.map((meta, idx) => (
          <tr key={idx}>
            <td>{meta.prompt}</td>
            <td>{meta.width}</td>
            <td>{meta.height}</td>
            <td>{meta.source_model || "-"}</td>
            <td>{meta.version || "-"}</td>
            <td>{meta.profile || "-"}</td>
            <td>{meta.job_id || "-"}</td>
            <td>{meta.created_date ? new Date(meta.created_date).toLocaleString() : "-"}</td>
            <td>{meta.author || "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default MetadataTable;

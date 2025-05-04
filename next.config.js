/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/extract-metadata',
        destination: 'http://localhost:8000/api/extract-metadata',
      },
    ];
  },
};

module.exports = nextConfig;

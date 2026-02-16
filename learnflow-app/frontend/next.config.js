/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  webpack: (config, { isServer }) => {
    if (isServer) {
      config.externals.push({
        pg: "commonjs pg",
        "pg-pool": "commonjs pg-pool",
        "pg-native": "commonjs pg-native",
      });
    }
    return config;
  },
};

module.exports = nextConfig;

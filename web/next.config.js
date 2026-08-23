/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    AGENT_URL: process.env.AGENT_URL
  }
}
module.exports = nextConfig

import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'LearnFlow',
  tagline: 'AI-Powered Python Tutoring Platform',
  favicon: 'img/favicon.ico',
  url: 'https://learnflow.dev',
  baseUrl: '/',
  organizationName: 'learnflow',
  projectName: 'learnflow-docs',
  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'LearnFlow',
      items: [
        { type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Docs' },
        { href: 'https://github.com/your-org/learnflow', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Built with Skills + MCP Code Execution`,
    },
    prism: {
      additionalLanguages: ['bash', 'python', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

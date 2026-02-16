import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Architecture',
      items: ['architecture/overview', 'architecture/services', 'architecture/events'],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: ['api/triage', 'api/concepts', 'api/code-runner', 'api/debug', 'api/exercise', 'api/progress', 'api/code-review'],
    },
    {
      type: 'category',
      label: 'Skills Library',
      items: ['skills/overview', 'skills/creating-skills'],
    },
    {
      type: 'category',
      label: 'Deployment',
      items: ['deployment/local', 'deployment/kubernetes', 'deployment/production'],
    },
  ],
};

export default sidebars;

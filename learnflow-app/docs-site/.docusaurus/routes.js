import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/',
    component: ComponentCreator('/', '44b'),
    routes: [
      {
        path: '/',
        component: ComponentCreator('/', 'd3c'),
        routes: [
          {
            path: '/',
            component: ComponentCreator('/', 'f32'),
            routes: [
              {
                path: '/api/code-review',
                component: ComponentCreator('/api/code-review', '01a'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/api/code-runner',
                component: ComponentCreator('/api/code-runner', 'e8d'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/api/concepts',
                component: ComponentCreator('/api/concepts', 'fa2'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/api/debug',
                component: ComponentCreator('/api/debug', '3e8'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/api/exercise',
                component: ComponentCreator('/api/exercise', '21b'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/api/progress',
                component: ComponentCreator('/api/progress', '261'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/api/triage',
                component: ComponentCreator('/api/triage', '75c'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/architecture/events',
                component: ComponentCreator('/architecture/events', 'd24'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/architecture/overview',
                component: ComponentCreator('/architecture/overview', 'f3c'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/architecture/services',
                component: ComponentCreator('/architecture/services', 'cac'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/deployment/kubernetes',
                component: ComponentCreator('/deployment/kubernetes', '926'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/deployment/local',
                component: ComponentCreator('/deployment/local', 'b6f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/deployment/production',
                component: ComponentCreator('/deployment/production', 'ecc'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/skills/creating-skills',
                component: ComponentCreator('/skills/creating-skills', '5eb'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/skills/overview',
                component: ComponentCreator('/skills/overview', 'f34'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/',
                component: ComponentCreator('/', '7da'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];

import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // Tutorial/documentation sidebar
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      link: {
        type: 'doc',
        id: 'getting-started/index',
      },
      items: [
        'getting-started/installation',
      ],
    },
  ],

  // API Reference sidebar - populated after running: pydoc-markdown
  apiSidebar: [
    'api/index',
  ],
};

export default sidebars;

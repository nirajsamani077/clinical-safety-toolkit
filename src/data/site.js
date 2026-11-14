// One place to change site-wide settings and the page order.
export const site = {
  name: 'Clinical Safety Toolkit',
  owner: 'Staffordshire Training Hub',
  author: 'Dr Niraj Samani, STH AI & Digital Health Ambassador',
  // Set to false when the content has been checked and the site goes live.
  draft: import.meta.env.PUBLIC_RELEASE !== '1',
  lastUpdated: '17 November 2026',
};

// Zones of the site. `live: false` shows a "coming soon" page.
export const zones = {
  adopt: { name: 'Adopting a tool', href: '/adopting-a-tool', live: true },
  cs: { name: 'Clinical safety', href: '/clinical-safety', live: true },
  ig: { name: 'Information governance', href: '/information-governance', live: true },
  ai: { name: 'AI policy', href: '/ai-policy', live: true },
  lib: { name: 'Explainers', href: '/explainers', live: true },
};

// The six tabs of the clinical safety zone, in reading order.
export const csPages = [
  { href: '/clinical-safety/understand', title: 'Understand', blurb: 'What clinical safety is, who does what, and how risk is scored.' },
  { href: '/clinical-safety/process', title: 'The process', blurb: 'Five stages, from first look to keeping it safe.' },
  { href: '/clinical-safety/worked-examples', title: 'Worked examples', blurb: 'An online consultation tool in full, plus an AI scribe and a built-in calculator.' },
  { href: '/clinical-safety/templates', title: 'Templates', blurb: 'Documents to read, download and adapt.' },
  { href: '/clinical-safety/after-go-live', title: 'After go-live', blurb: 'Incident logs, monitoring and when to reassess.' },
  { href: '/clinical-safety/help', title: 'Help', blurb: 'Finding a CSO, training and common questions.' },
];

// The six tabs of the information governance zone.
export const igPages = [
  { href: '/information-governance/understand', title: 'Understand', blurb: 'Data protection in plain English, the rules, and who does what.' },
  { href: '/information-governance/dpia', title: 'The DPIA', blurb: 'When you need one, how to do it, and Oakfield’s example.' },
  { href: '/information-governance/suppliers', title: 'Suppliers', blurb: 'Data processing agreements and the questions to ask.' },
  { href: '/information-governance/telling-patients', title: 'Telling patients', blurb: 'Privacy notices, objections and the national data opt-out.' },
  { href: '/information-governance/after-go-live', title: 'After go-live', blurb: 'Data breaches, records, reviews and ending a contract.' },
  { href: '/information-governance/help', title: 'Help', blurb: 'Finding a DPO, training and common questions.' },
];

// The three tabs of the AI policy zone.
export const aiPages = [
  { href: '/ai-policy/understand', title: 'Understand', blurb: 'What counts as AI, why a policy matters, and how it fits with the rest.' },
  { href: '/ai-policy/your-policy', title: 'Your policy', blurb: 'An example policy to adapt, what goes in your tool register, and a staff card.' },
  { href: '/ai-policy/cqc-readiness', title: 'CQC readiness', blurb: 'What inspectors may ask for, as a checklist.' },
];

// The explainers: one short page per term you'll meet. `owner` drives the filter on the hub.
export const libPages = [
  { href: '/explainers/dcb0129-and-dcb0160', title: 'DCB0129 and DCB0160', owner: ['supplier', 'practice'], blurb: 'The two clinical safety standards, and how the supplier’s work feeds into yours.' },
  { href: '/explainers/dtac', title: 'DTAC', owner: ['supplier'], blurb: 'The NHS checklist suppliers fill in. You read it before you buy.' },
  { href: '/explainers/medical-devices', title: 'Medical devices', owner: ['supplier'], blurb: 'When software counts as a medical device, and what that means for AI scribes.' },
  { href: '/explainers/dspt', title: 'DSPT', owner: ['practice'], blurb: 'Your yearly data security check, and where new tools come into it.' },
  { href: '/explainers/cyber-security', title: 'Cyber security', owner: ['practice', 'icb', 'supplier'], blurb: 'How attackers get in, who locks which door, and what Cyber Essentials is.' },
  { href: '/explainers/im1', title: 'IM1 and GP system links', owner: ['supplier'], blurb: 'How other tools read from and write to your clinical system.' },
  { href: '/explainers/ai-scribe-registry', title: 'The AI scribe registry', owner: ['practice'], blurb: 'What being on NHS England’s list means, and what it doesn’t.' },
  { href: '/explainers/large-language-models', title: 'Large language models', owner: ['everyone'], blurb: 'How AI chatbots and scribes produce text, and why they sometimes make things up.' },
];

export const extraPages = [
  { href: '/whats-changing', title: "What's changing" },
  { href: '/glossary', title: 'Glossary' },
  { href: '/sources', title: 'Sources and permissions' },
  { href: '/about', title: 'About this toolkit' },
  { href: '/disclaimer', title: 'Disclaimer and privacy' },
];

'use client';

import { useEffect, useMemo, useState } from 'react';

const services = [
  ['Administrative Support', 'Day-to-day task support, organized follow-through, and dependable assistance for busy teams.'],
  ['Data Entry', 'Accurate spreadsheet updates, records organization, cleanup, and structured information handling.'],
  ['Email & Calendar', 'Inbox organization, scheduling support, reminders, and calendar maintenance.'],
  ['File Management', 'Logical naming, folder organization, document handling, and easy-to-find records.'],
  ['Internet Research', 'Focused online research, information gathering, comparison, and clean summaries.'],
  ['Customer Support', 'Professional, respectful support backed by real-world customer-facing experience.'],
];

const skills = [
  'Google Workspace',
  'Microsoft Office / 365',
  'Google Sheets',
  'Google Calendar',
  'Canva',
  'Monday.com',
  'ChatGPT',
  'File Management',
  'Internet Research',
  'Data Entry',
  'Customer Service',
  'Administrative Support',
];

const projects = [
  {
    code: '01',
    title: 'Administrative Data Tracker',
    type: 'Spreadsheet / Data Entry',
    body: 'A structured sample tracker demonstrating organized records, clean formatting, status monitoring, and detail-focused data handling.',
    tags: ['Sheets', 'Data Entry', 'Organization'],
  },
  {
    code: '02',
    title: 'Inventory Coordination Sheet',
    type: 'Operations / Records',
    body: 'A sample inventory and coordination workflow designed to keep records clear, searchable, and easier to review.',
    tags: ['Excel', 'Inventory', 'Accuracy'],
  },
  {
    code: '03',
    title: 'Calendar Scheduling System',
    type: 'Calendar Management',
    body: 'A visual scheduling sample that demonstrates event organization, time blocking, reminders, and calendar maintenance.',
    tags: ['Google Calendar', 'Scheduling', 'Planning'],
  },
  {
    code: '04',
    title: 'Delivery & Operations Records',
    type: 'Real-World Workflow',
    body: 'Operational records based on delivery work experience, highlighting time management, navigation, accuracy, and independent execution.',
    tags: ['Operations', 'Records', 'Time Management'],
  },
  {
    code: '05',
    title: 'APEX — Personal AI Companion',
    type: 'Personal Technology Project',
    body: 'A personal AI companion project exploring a lightweight, local-first architecture, persistent memory, modular automation, and a futuristic desktop interface.',
    tags: ['AI Workflow', 'UI Concept', 'Automation'],
    featured: true,
  },
];

const experience = [
  {
    year: '2022 — Present',
    role: 'Foodpanda Delivery Rider',
    detail:
      'Handles daily deliveries independently while managing navigation, customer coordination, time-sensitive tasks, and accurate order handling.',
  },
  {
    year: 'Earlier Experience',
    role: 'Sales Demonstrator • Receiving & Dispatching • E-bike Technician • Deck Cadet',
    detail:
      'Built transferable strengths in customer service, responsibility, troubleshooting, physical and digital record handling, adaptability, and working under pressure.',
  },
];

function ArrowIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 12h14M13 6l6 6-6 6" />
    </svg>
  );
}

function MailIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18v12H3z" />
      <path d="m3 7 9 7 9-7" />
    </svg>
  );
}

export default function Home() {
  const [copied, setCopied] = useState(false);
  const [visible, setVisible] = useState(new Set());
  const email = 'acatanguijr29@gmail.com';

  const dots = useMemo(
    () =>
      Array.from({ length: 36 }, (_, i) => ({
        id: i,
        x: ((i * 37) % 101) + '%',
        y: ((i * 61) % 97) + '%',
        delay: `${(i % 9) * 0.35}s`,
      })),
    []
  );

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setVisible((prev) => new Set(prev).add(entry.target.id));
          }
        });
      },
      { threshold: 0.12 }
    );

    document.querySelectorAll('[data-reveal]').forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const handler = (event) => {
      document.documentElement.style.setProperty('--mouse-x', `${event.clientX}px`);
      document.documentElement.style.setProperty('--mouse-y', `${event.clientY}px`);
    };
    window.addEventListener('pointermove', handler, { passive: true });
    return () => window.removeEventListener('pointermove', handler);
  }, []);

  const reveal = (id) => (visible.has(id) ? 'reveal is-visible' : 'reveal');

  async function copyEmail() {
    try {
      await navigator.clipboard.writeText(email);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      window.location.href = `mailto:${email}`;
    }
  }

  return (
    <main>
      <div className="cursor-glow" />
      <div className="ambient-grid" aria-hidden="true" />
      <div className="star-field" aria-hidden="true">
        {dots.map((dot) => (
          <span key={dot.id} style={{ left: dot.x, top: dot.y, animationDelay: dot.delay }} />
        ))}
      </div>

      <header className="nav-wrap">
        <nav className="nav shell">
          <a className="brand" href="#top" aria-label="Home">
            <span>AC</span>
            <strong>Ananias.</strong>
          </a>
          <div className="nav-links">
            <a href="#work">Work</a>
            <a href="#skills">Skills</a>
            <a href="#experience">Experience</a>
          </div>
          <a className="nav-cta" href={`mailto:${email}`}>
            Let&apos;s work
            <ArrowIcon />
          </a>
        </nav>
      </header>

      <section id="top" className="hero shell">
        <div className="hero-copy">
          <div className="eyebrow"><span className="status-dot" /> Open to remote opportunities</div>
          <h1>
            Helping business owners
            <span className="shine-text"> stay organized.</span>
          </h1>
          <p className="hero-lead">
            I&apos;m <strong>Ananias Jr. D. Catangui</strong>, an entry-level General Administrative
            Virtual Assistant focused on dependable support, accurate data handling, and organized workflows.
          </p>
          <div className="hero-actions">
            <a className="button primary" href="#work">Explore my work <ArrowIcon /></a>
            <button className="button ghost" type="button" onClick={copyEmail}>
              <MailIcon /> {copied ? 'Email copied!' : 'Copy email'}
            </button>
          </div>
          <div className="hero-meta">
            <div><span>Based in</span><strong>Philippines</strong></div>
            <div><span>Focus</span><strong>Admin • Data • Support</strong></div>
            <div><span>Goal</span><strong>Long-term remote role</strong></div>
          </div>
        </div>

        <div className="portrait-stage" aria-label="Portrait of Ananias Jr. D. Catangui">
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="portrait-halo" />
          <div className="portrait-frame">
            <img src="https://raw.githubusercontent.com/herkeeper445-sys/ananias-va-portfolio/main/public/ananias-profile.webp" alt="Ananias Jr. D. Catangui" />
            <div className="portrait-overlay" />
          </div>
          <div className="floating-card card-a">
            <span>GENERAL VA</span>
            <strong>Organized support</strong>
          </div>
          <div className="floating-card card-b">
            <span>WORK STYLE</span>
            <strong>Reliable • Adaptable</strong>
          </div>
        </div>
      </section>

      <section className="marquee" aria-label="Skills highlights">
        <div className="marquee-track">
          {[...skills, ...skills].map((skill, i) => <span key={`${skill}-${i}`}>{skill}<b>✦</b></span>)}
        </div>
      </section>

      <section id="about" className="section shell two-col">
        <div id="about-title" data-reveal className={reveal('about-title')}>
          <p className="section-kicker">01 / About me</p>
          <h2>New to VA work.<br /><span>Not new to responsibility.</span></h2>
        </div>
        <div id="about-copy" data-reveal className={`${reveal('about-copy')} about-copy`}>
          <p>
            I&apos;m building my career in remote administrative support using the discipline and practical skills I&apos;ve developed through real-world work: staying organized, meeting time-sensitive requirements, serving customers, solving problems, and working independently.
          </p>
          <p>
            I learn processes quickly, follow instructions carefully, and value consistency. I&apos;m looking for a company or client where I can contribute, improve, and stay for the long term as long as my help is needed.
          </p>
        </div>
      </section>

      <section className="section shell">
        <div id="services-title" data-reveal className={reveal('services-title')}>
          <p className="section-kicker">02 / What I can support</p>
          <h2>Practical help for <span>busy workflows.</span></h2>
        </div>
        <div className="service-grid">
          {services.map(([title, body], index) => (
            <article id={`service-${index}`} data-reveal className={`${reveal(`service-${index}`)} service-card`} key={title}>
              <div className="service-number">0{index + 1}</div>
              <h3>{title}</h3>
              <p>{body}</p>
              <div className="service-line" />
            </article>
          ))}
        </div>
      </section>

      <section id="work" className="section shell">
        <div className="section-head">
          <div id="work-title" data-reveal className={reveal('work-title')}>
            <p className="section-kicker">03 / Selected work</p>
            <h2>Samples that show <span>how I work.</span></h2>
          </div>
          <p id="work-note" data-reveal className={`${reveal('work-note')} section-note`}>
            Practice and personal projects built to demonstrate organization, accuracy, scheduling, operations thinking, and technology curiosity.
          </p>
        </div>

        <div className="project-grid">
          {projects.map((project, index) => (
            <article id={`project-${index}`} data-reveal className={`${reveal(`project-${index}`)} project-card ${project.featured ? 'featured' : ''}`} key={project.title}>
              <div className="project-top"><span>{project.code}</span><span>{project.type}</span></div>
              <div>
                <h3>{project.title}</h3>
                <p>{project.body}</p>
              </div>
              <div className="tag-row">{project.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
            </article>
          ))}
        </div>
      </section>

      <section id="skills" className="section shell skill-section">
        <div id="skills-title" data-reveal className={reveal('skills-title')}>
          <p className="section-kicker">04 / Toolkit</p>
          <h2>Comfortable with the tools that <span>keep work moving.</span></h2>
        </div>
        <div className="skill-cloud">
          {skills.map((skill, index) => (
            <span id={`skill-${index}`} data-reveal className={reveal(`skill-${index}`)} key={skill}>{skill}</span>
          ))}
        </div>
      </section>

      <section id="experience" className="section shell experience-section">
        <div id="experience-title" data-reveal className={reveal('experience-title')}>
          <p className="section-kicker">05 / Experience</p>
          <h2>Transferable experience,<br /><span>ready for remote work.</span></h2>
        </div>
        <div className="timeline">
          {experience.map((item, index) => (
            <article id={`exp-${index}`} data-reveal className={reveal(`exp-${index}`)} key={item.role}>
              <div className="timeline-dot" />
              <span className="timeline-year">{item.year}</span>
              <h3>{item.role}</h3>
              <p>{item.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section shell commitment">
        <div id="commitment" data-reveal className={`${reveal('commitment')} commitment-card`}>
          <span className="big-quote">“</span>
          <p>
            I&apos;m not looking for a temporary VA title. I&apos;m looking for the opportunity to become useful, dependable, and valuable to a team over time.
          </p>
          <div><span>ANANIAS JR. D. CATANGUI</span><strong>General Administrative VA</strong></div>
        </div>
      </section>

      <section id="contact" className="section shell contact-section">
        <div id="contact-card" data-reveal className={`${reveal('contact-card')} contact-card`}>
          <p className="section-kicker">06 / Let&apos;s connect</p>
          <h2>Need an organized extra pair of hands?</h2>
          <p>I&apos;m ready to learn your workflow and help you keep the important details under control.</p>
          <div className="contact-actions">
            <a className="button light" href={`mailto:${email}?subject=Virtual%20Assistant%20Opportunity`}>Email me <ArrowIcon /></a>
            <button className="email-chip" type="button" onClick={copyEmail}>{copied ? 'Copied!' : email}</button>
          </div>
        </div>
      </section>

      <footer className="footer shell">
        <div className="brand"><span>AC</span><strong>Ananias.</strong></div>
        <p>General Administrative Virtual Assistant • Philippines</p>
        <a href="#top">Back to top ↑</a>
      </footer>
    </main>
  );
}

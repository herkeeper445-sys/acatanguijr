import styles from './resume.module.css';

export const metadata = {
  title: 'Resume | Ananias Jr. D. Catangui',
  description: 'Resume of Ananias Jr. D. Catangui, Entry-Level General Administrative Virtual Assistant.',
};

const jobs = [
  {
    role: 'Foodpanda Delivery Rider',
    company: 'Foodpanda Philippines',
    dates: 'June 10, 2022 – Present',
    bullets: [
      'Manage daily delivery schedules and route priorities while working independently in a time-sensitive environment.',
      'Verify orders, addresses, customer instructions, and payment details to maintain accuracy and minimize errors.',
      'Use mobile navigation and delivery applications to coordinate routes, status updates, and customer communication.',
      'Handle cash and digital payments responsibly while providing professional customer service.',
    ],
  },
  {
    role: 'Sales Demonstrator',
    company: 'Rusty Lopez – SM Megamall',
    dates: 'Dec. 1, 2017 – Feb. 1, 2018',
    bullets: [
      'Assisted customers with product inquiries, recommendations, and purchase decisions.',
      'Maintained organized merchandise displays, monitored stock availability, and supported replenishment.',
      'Processed sales transactions and coordinated with team members to support daily store operations.',
    ],
  },
  {
    role: 'Receiving Dispatching Unit',
    company: 'Free Choice Mart',
    dates: 'May 5, 2017 – Oct. 20, 2017',
    bullets: [
      'Received, checked, documented, and organized incoming deliveries and inventory records.',
      'Performed stock counts, identified discrepancies, and supported accurate replenishment.',
      'Maintained an orderly stockroom to improve product retrieval and day-to-day operations.',
    ],
  },
  {
    role: 'E-Bike Technician',
    company: 'Romai Electric Bike',
    dates: 'Oct. 28, 2015 – Apr. 29, 2016',
    bullets: [
      'Diagnosed and repaired electrical and mechanical issues across multiple e-bike models.',
      'Provided field-service support at customer locations when units could not travel.',
      'Maintained repair records, managed tools and spare parts, and explained service status to customers.',
    ],
  },
  {
    role: 'Deck Cadet',
    company: 'M/V Star Ferry III',
    dates: 'Oct. 8, 2014 – Oct. 15, 2015',
    bullets: [
      'Assisted senior officers with operational duties, recordkeeping, documentation, and assigned administrative tasks.',
      'Followed maritime safety procedures and worked reliably in a demanding, fast-paced team environment.',
      'Demonstrated attention to detail, discipline, and responsibility during vessel operations.',
    ],
  },
  {
    role: 'Stockman',
    company: 'Rusty Lopez – Iriga City',
    dates: 'Jun. 8, 2013 – Dec. 8, 2013',
    bullets: [
      'Received and inspected deliveries, organized inventory, and maintained accurate stock levels.',
      'Prepared merchandise for display and replenished store inventory as needed.',
      'Maintained an orderly stockroom and supported staff with daily inventory tasks.',
    ],
  },
];

export default function ResumePage() {
  return (
    <main className={styles.page}>
      <div className={styles.wrap}>
        <div className={styles.topbar}>
          <a className={styles.back} href="/">← Back to portfolio</a>
          <a className={styles.action} href="mailto:acatanguijr29@gmail.com?subject=Virtual%20Assistant%20Opportunity">Contact me</a>
        </div>

        <article className={styles.sheet}>
          <header className={styles.header}>
            <h1>ANANIAS JR. D. CATANGUI</h1>
            <h2>Entry-Level General Administrative Virtual Assistant</h2>
            <div className={styles.contact}>
              <span>Iriga City, Camarines Sur, Philippines</span>
              <span>•</span>
              <a href="tel:+639389114841">+63 938 911 4841</a>
              <span>•</span>
              <a href="mailto:acatanguijr29@gmail.com">acatanguijr29@gmail.com</a>
            </div>
            <div className={styles.links}>
              <a href="https://www.linkedin.com/in/ananias-jr-catangui-7b424a129" target="_blank" rel="noreferrer">LinkedIn</a>
              <a href="https://acatanguijrportfolio-beta.vercel.app/" target="_blank" rel="noreferrer">Portfolio Website</a>
            </div>
          </header>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Professional Profile</h3>
            <p>
              Entry-level General Administrative Virtual Assistant candidate with no previous professional VA work experience. Currently building foundational knowledge through self-study and hands-on practice in administrative workflows, data entry, file organization, internet research, email and calendar basics, digital productivity tools, Canva, ChatGPT, and basic workflow automation. Brings several years of transferable experience from logistics, retail, customer service, technical service, inventory, and documentation, including working independently, meeting deadlines, maintaining accuracy, and assisting customers. Seeking a first VA opportunity where these transferable strengths and developing digital skills can be applied and improved.
            </p>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Foundational VA Knowledge & Transferable Strengths</h3>
            <p>
              Foundational knowledge / practice: Administrative Support Basics • Data Entry • File Organization • Internet Research • Email & Calendar Workflow Basics • Basic Documentation • Workflow Automation Basics
            </p>
            <p className={styles.toolLine}>
              Transferable strengths: Customer Service • Schedule Management • Record Accuracy • Inventory Coordination • Problem Solving • Independent Work
            </p>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Tools — Learning & Practice Level</h3>
            <p>
              Microsoft Office • Google Workspace • Canva • ChatGPT • Monday.com • n8n (beginner / workflow practice) • ElevenLabs • Ideogram • Fliki • Python (beginner / personal project use)
            </p>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Practice Projects & Self-Directed Learning</h3>
            <div className={styles.block}>
              <h3>VA Portfolio & Canva Sample Projects</h3>
              <p className={styles.meta}>Self-directed practice | Current — not professional client work</p>
              <ul className={styles.list}>
                <li>Created portfolio samples to demonstrate organization, presentation, and digital content skills, including social media graphics, posters, quote designs, and short-form video concepts.</li>
                <li>Built and published a personal portfolio website to present services, tools, sample work, transferable experience, and contact information.</li>
              </ul>
            </div>
            <div className={styles.block}>
              <h3>APEX Personal AI Companion</h3>
              <p className={styles.meta}>Ongoing personal learning project — not professional development experience</p>
              <ul className={styles.list}>
                <li>Using ChatGPT, coding assistance, and beginner-level Python while learning how to plan an AI companion interface, organize feature requirements, test ideas, and troubleshoot problems.</li>
                <li>This project is included to show curiosity, self-learning, practical AI-tool use, and documentation—not to claim professional software-development experience.</li>
              </ul>
            </div>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Professional Experience</h3>
            {jobs.map((job) => (
              <div className={styles.block} key={`${job.role}-${job.dates}`}>
                <h3>{job.role}</h3>
                <p className={styles.meta}>{job.company} | {job.dates}</p>
                <ul className={styles.list}>
                  {job.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}
                </ul>
              </div>
            ))}
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Education</h3>
            <p>Bachelor of Science in Marine Transportation (BSMT)</p>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Languages</h3>
            <p>Filipino — Native • English — Intermediate</p>
          </section>
        </article>

        <p className={styles.footer}>Ananias Jr. D. Catangui • General Administrative VA Resume</p>
      </div>
    </main>
  );
}

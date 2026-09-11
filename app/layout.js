import './globals.css';
import './portrait-particles.css';
import './portfolio-v2.css';

export const metadata = {
  title: 'Ananias Jr. D. Catangui | General Administrative Virtual Assistant',
  description:
    'Portfolio of Ananias Jr. D. Catangui — entry-level General Administrative Virtual Assistant focused on organized, dependable remote support.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

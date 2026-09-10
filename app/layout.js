import './globals.css';

export const metadata = {
  title: 'Ananias Jr. D. Catangui | General Administrative VA',
  description: 'Portfolio of Ananias Jr. D. Catangui, an entry-level General Administrative Virtual Assistant based in the Philippines.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

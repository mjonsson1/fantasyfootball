import React from 'react';
import WelcomeBanner from './WelcomeBanner';
import QuickAccess from './QuickAccess';
import Footer from './Footer';

function Home() {
  return (
    <div>
      <WelcomeBanner />
      <QuickAccess />
      <Footer />
    </div>
  );
}

export default Home;

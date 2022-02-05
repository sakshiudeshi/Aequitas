import React from 'react';
import Footer from '../components/Footer';
import Header from '../components/Header';
import OurNavbar from '../components/OurNavbar';

export default function AboutUsScreen() {
  return (
    <div>
      <OurNavbar></OurNavbar>
      <Header child={<h1 className="display-4">About Us</h1>}></Header>
      <Footer></Footer>
    </div>
    
  )
}
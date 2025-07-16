import React, { useState, useEffect } from 'react';
import Motivation from './Motivation';
import Prerequisites from './Prerequisites';
import StandardInstall from './StandardInstall';
import Cloud2EdgeInstall from './Cloud2EdgeInstall';
import './App.css';

const App = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSectionChange = (section) => {
    setActiveSection(section);
    if (section !== 'home') {
      scrollToSection('installation-guide');
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    alert('Thank you for your message! We\'ll get back to you soon.');
    e.target.reset();
  };

  return (
    <div className="App">
      {/* Navigation */}
      <nav className={`navbar navbar-expand-lg fixed-top ${isScrolled ? 'scrolled' : ''}`}>
        <div className="container">
          <a className="navbar-brand" href="#home" onClick={() => handleSectionChange('home')}>
            <img 
              src="https://reroutlab.org/images/iciclelogo.jpg" 
              style={{width: '11vw', height: '100px',objectFit: 'contain'}} 
              alt="Logo of the ICICLE AI Institute"
            />
            <img 
              src="https://ohiosoyadvantage.com/wp-content/uploads/2021/02/ohio-soybean-council-logo.png" 
              style={{width: '11vw', height: '100px',objectFit: 'contain'}} 
              alt="Logo of the ICICLE AI Institute"
            />
            ICICLE OpenPass
          </a>
          
          <button 
            className="navbar-toggler border-0" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto align-items-center">
              <li className="nav-item">
                <a className="nav-link" href="#home" onClick={() => handleSectionChange('home')}>Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#mission" onClick={() => scrollToSection('mission')}>Mission</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#product" onClick={() => scrollToSection('product')}>OpenPASS</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#download" onClick={() => scrollToSection('download')}>Download</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#contact" onClick={() => scrollToSection('contact')}>Contact</a>
              </li>
              <li className="nav-item">
                <a 
                  className="nav-link" 
                  href="#installation-guide" 
                  onClick={() => handleSectionChange('motivation')}
                >
                  Installation Guide
                </a>
              </li>
              <li className="nav-item ms-2">
                <a href="mailto:contact@icicle-agriculture.com" className="navbar-email">
                  <i className="fas fa-envelope me-2"></i>Get in Touch
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="hero-section">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <div className="hero-content">
                <h1 className="hero-title">AI for All</h1>
                <p className="hero-subtitle">
                  Democratizing next-generation cyberinfrastructure to bring cutting-edge AI 
                  and realize the digital agriculture revolution
                </p>
                <button 
                  className="btn btn-hero" 
                  onClick={() => scrollToSection('product')}
                >
                  <i className="fas fa-rocket me-2"></i>
                  Discover OpenPASS
                </button>
              </div>
            </div>
            <div className="col-lg-6">
              <img 
                src="https://user-images.githubusercontent.com/69735000/210019352-a3d5a913-d351-40d0-bb96-14f1ccb9da0b.png" 
                alt="Digital Agriculture Technology" 
                className="img-fluid rounded-3"
              />
            </div>
          </div>

          {/* Feature Cards */}
          <div className="hero-features">
            <div className="row g-4">
              <div className="col-md-4">
                <div className="feature-card">
                  <div className="feature-icon">
                    <i className="fas fa-map-marked-alt"></i>
                  </div>
                  <h5 className="text-white">Autonomous Mapping</h5>
                  <p>Map fields autonomously and continuously with precision</p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="feature-card">
                  <div className="feature-icon">
                    <i className="fas fa-brain"></i>
                  </div>
                  <h5 className="text-white">Smart Decisions</h5>
                  <p>Make better crop management decisions with AI insights</p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="feature-card">
                  <div className="feature-icon">
                    <i className="fas fa-microchip"></i>
                  </div>
                  <h5 className="text-white">Edge Computing</h5>
                  <p>State-of-the-art edge computing for real-time processing</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section id="mission" className="mission-section">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto text-center">
              <h2 className="section-title">What is Digital Agriculture?</h2>
              <div className="mission-content">
                <p className="lead mb-4">
                  <span className="highlight">9 million children</span> suffer from food insecurity. 
                  Migrant workers in food production die, on average, 38 years sooner than well-off Americans.
                </p>
                <p className="mb-4">
                  <strong>Digital Agriculture</strong> uses AI, IoT sensors, edge computing, and agricultural 
                  engineering to transform crop and farm management, increasing yield, improving working 
                  conditions, and remedying crop health problems quickly and precisely.
                </p>
                <p className="mb-4">
                  <strong>What is cyberinfrastructure (CI)?</strong> CI includes the software and hardware 
                  needed to realize digital agriculture. Unfortunately, CI needed for advanced AI systems 
                  could be more cost-effective, limiting its impact.
                </p>
                <p>
                  We design, prototype, and deploy accessible and affordable CI for digital agriculture - 
                  <span className="highlight">AI for ALL</span>.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Product Section */}
      <section id="product" className="product-section">
        <div className="container">
          <div className="row">
            <div className="col-lg-10 mx-auto text-center">
              <h2 className="section-title">
                <strong>OpenPASS:</strong> Open-Source, Plug-and-Play Aerial Crop Scouting
              </h2>
              <p className="lead mb-5">
                OpenPASS is an open-source web and mobile application that allows farmers, consultants, 
                and researchers to automatically deploy software-piloted drones for rapid aerial scouting 
                of soybean crop health. Our deep-learning software can accurately characterize severe 
                defoliation from aerial photos and map defoliation levels across a whole field with 
                high confidence <strong>in minutes to hours</strong>.
              </p>
            </div>
          </div>

          <div className="product-grid">
            <div className="product-card">
              <div className="step-number">1</div>
              <img 
                src="https://cdn.thewirecutter.com/wp-content/media/2022/10/drones-2048px-0706-2x1-1.jpg" 
                alt="Unmanned Aerial System" 
                className="product-image"
              />
              <h4 className="product-title">Unmanned Aerial System</h4>
              <p>We ship our drones and infrastructure to you. Simply unpack, link your smartphone, and start missions.</p>
            </div>

            <div className="product-card">
              <div className="step-number">2</div>
              <img 
                src="https://reroutlab.org/images/fieldmap.jpg" 
                alt="Autonomous Field Mapping" 
                className="product-image"
              />
              <h4 className="product-title">Autonomous Field Mapping</h4>
              <p>Set GPS boundaries and crop conditions. Our system flies autonomously and produces field maps in real-time.</p>
            </div>

            <div className="product-card">
              <div className="step-number">3</div>
              <img 
                src="https://reroutlab.org/images/soybeanfield.jpg" 
                alt="Data-Driven Field Management" 
                className="product-image"
              />
              <h4 className="product-title">Data-Driven Management</h4>
              <p>Use maps to inform pesticide and fertilizer applications. Upload our maps to compatible sprayers.</p>
            </div>

            <div className="product-card">
              <div className="step-number">4</div>
              <img 
                src="https://miro.medium.com/max/1400/1*e-f-6BRq4-Bv4jW6CSjiTg.webp" 
                alt="High Performance Computing" 
                className="product-image"
              />
              <h4 className="product-title">Advanced Computing</h4>
              <p>Optionally send data to ICICLE for analysis using efficient, high-performance computing infrastructure.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Download Section */}
      <section id="download" className="download-section">
        <div className="container">
          <h2 className="section-title text-center text-white mb-4">Download OpenPASS</h2>
          <p className="lead text-center mb-4">
            Get started with OpenPASS today. Available for multiple platforms.
          </p>
          <div className="download-buttons">
            <a href="#" className="btn-download">
              <i className="fab fa-github"></i>
              <div>
                <div>View on</div>
                <strong>GitHub</strong>
              </div>
            </a>
          </div>
        </div>
      </section>

      {/* Installation Guide Section */}
      <section id="installation-guide" className="installation-guide-section">
        <div className="container">
          <div className="row">
            <div className="col-lg-3">
              <div className="installation-nav">
                <h4 className="nav-title">Installation Guide</h4>
                <div className="nav-progress">
                  <div className={`progress-step ${(activeSection === 'motivation' || (!['prerequisites', 'standard', 'cloud2edge'].includes(activeSection))) ? 'active' : ''}`}>
                    <div className="step-number">1</div>
                    <div className="step-content">
                      <button 
                        className="step-button"
                        onClick={() => handleSectionChange('motivation')}
                      >
                        Motivation
                      </button>
                    </div>
                  </div>
                  <div className={`progress-step ${activeSection === 'prerequisites' ? 'active' : ''}`}>
                    <div className="step-number">2</div>
                    <div className="step-content">
                      <button 
                        className="step-button"
                        onClick={() => handleSectionChange('prerequisites')}
                      >
                        Prerequisites
                      </button>
                    </div>
                  </div>
                  <div className={`progress-step ${activeSection === 'standard' ? 'active' : ''}`}>
                    <div className="step-number">3</div>
                    <div className="step-content">
                      <button 
                        className="step-button"
                        onClick={() => handleSectionChange('standard')}
                      >
                        Standard Install
                      </button>
                    </div>
                  </div>
                  <div className={`progress-step ${activeSection === 'cloud2edge' ? 'active' : ''}`}>
                    <div className="step-number">4</div>
                    <div className="step-content">
                      <button 
                        className="step-button"
                        onClick={() => handleSectionChange('cloud2edge')}
                      >
                        Cloud2Edge Install
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-lg-9">
              <div className="installation-content">
                {(activeSection === 'motivation' || (!['prerequisites', 'standard', 'cloud2edge'].includes(activeSection))) && 
                  <Motivation onNext={() => handleSectionChange('prerequisites')} />}
                {activeSection === 'prerequisites' && (
                  <Prerequisites 
                    onNext={() => handleSectionChange('standard')} 
                    onPrev={() => handleSectionChange('motivation')} 
                  />
                )}
                {activeSection === 'standard' && (
                  <StandardInstall 
                    onNext={() => handleSectionChange('cloud2edge')} 
                    onPrev={() => handleSectionChange('prerequisites')} 
                  />
                )}
                {activeSection === 'cloud2edge' && (
                  <Cloud2EdgeInstall 
                    onPrev={() => handleSectionChange('standard')} 
                  />
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact-section">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <div className="text-center mb-5">
                <h2 className="section-title text-white">Get in Touch</h2>
                <p className="lead">
                  Interested in using OpenPASS? We'd love to hear from you.
                </p>
              </div>
              
              <div className="contact-form">
                <form onSubmit={handleFormSubmit}>
                  <div className="row g-3">
                    <div className="col-md-6">
                      <input type="text" className="form-control" placeholder="Your Name" required />
                    </div>
                    <div className="col-md-6">
                      <input type="email" className="form-control" placeholder="Your Email" required />
                    </div>
                    <div className="col-md-6">
                      <input type="text" className="form-control" placeholder="Organization" />
                    </div>
                    <div className="col-md-6">
                      <select className="form-control" required>
                        <option value="">Select Interest</option>
                        <option value="farmer">Farmer</option>
                        <option value="researcher">Researcher</option>
                        <option value="consultant">Consultant</option>
                        <option value="developer">Developer</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                    <div className="col-12">
                      <textarea 
                        className="form-control" 
                        rows="5" 
                        placeholder="Tell us about your project or how you'd like to use OpenPASS" 
                        required
                      ></textarea>
                    </div>
                    <div className="col-12 text-center">
                      <button type="submit" className="btn btn-contact">
                        <i className="fas fa-paper-plane me-2"></i>
                        Send Message
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="row">
            <div className="col-12 text-center">
              <p>&copy; 2025 ICICLE Digital Agriculture. All rights reserved.</p>
              <p>
                <a href="https://icicle.osu.edu/" className="text-light me-3">ICICLE AI Institute</a>
                <a href="#" className="text-light me-3">Privacy Policy</a>
                <a href="#" className="text-light">Terms of Service</a>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
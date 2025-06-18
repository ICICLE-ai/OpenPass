import React, { useState } from 'react';

const Cloud2EdgeInstall = ({ onPrev }) => {
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="content-section cloud2edge-install-section">
      <div className="content-header">
        <div className="step-indicator">
          <span className="step-number">04</span>
          <span className="step-label">Cloud2Edge Install</span>
        </div>
        <h2 className="content-title">Cloud2Edge Installation</h2>
        <p className="content-subtitle">
          Advanced deployment for distributed computing and cloud integration
        </p>
      </div>

      <div className="content-body">
        <div className="cloud2edge-simple-content">
          <p className="cloud2edge-intro-text">
            <strong>Advanced instructions to use the computing continuum.</strong>
          </p>

          <p className="jetstream-description">
            <strong>OpenPASS can use cloud servers provided by JetStream 2 to run AI models that enhance aerial crop scouting.</strong> 
            Instructions to access this operating mode are coming soon.
          </p>
        </div>

        <div className="navigation-buttons">
          <button className="btn btn-prev" onClick={onPrev}>
            <i className="fas fa-arrow-left"></i>
            <span>Previous: Standard Install</span>
          </button>
          
          <div className="completion-status">
            <div className="status-icon">
              <i className="fas fa-clock"></i>
            </div>
            <span>Coming Soon</span>
          </div>
          
          <a href="mailto:contact@icicle-agriculture.com" className="btn btn-contact">
            <span>Contact for Updates</span>
            <i className="fas fa-envelope"></i>
          </a>
        </div>
      </div>

      <div className="progress-indicator">
        <div className="progress-bar">
          <div className="progress-fill" style={{width: '100%'}}></div>
        </div>
        <span className="progress-text">Step 4 of 4 - Complete!</span>
      </div>

      <div className="openpass-footer">
        <div className="footer-content">
          <p>
            <strong>OpenPASS</strong> is a research product from the <strong>ReRout Lab at the Ohio State University</strong>. 
            The scripts and code made available through this page are released under the <strong>Academic Free License v3.0 (Open Source Initiative)</strong>.
          </p>
          <div className="disclaimer">
            <p>
              <strong>Note:</strong> OpenPASS is provided under this License on an "AS IS" BASIS and WITHOUT WARRANTY, either express or implied, 
              including, without limitation, the warranties of non-infringement, merchantability or fitness for a particular purpose. 
              THE ENTIRE RISK AS TO THE QUALITY OF THE ORIGINAL WORK IS WITH YOU. This DISCLAIMER OF WARRANTY constitutes an essential part of this License. 
              Under no circumstances and under no legal theory, whether in tort (including negligence), contract, or otherwise, shall the Licensor be liable 
              to anyone for any indirect, special, incidental, or consequential damages of any character arising as a result of this License or the use of 
              the Original Work including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all 
              other commercial damages or losses.
            </p>
            <p>
              OpenPASS is provided as an educational tool. To the best of our knowledge, OpenPASS does not improperly share restricted content. 
              If you are aware of software that is improperly included in this tool, please contact us.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cloud2EdgeInstall;
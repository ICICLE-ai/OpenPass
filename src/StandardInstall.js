import React, { useState } from 'react';

const StandardInstall = ({ onNext, onPrev }) => {
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  return (
    <div className="content-section standard-install-section">
      <div className="content-header">
        <div className="step-indicator">
          <span className="step-number">03</span>
          <span className="step-label">Standard Install</span>
        </div>
        <h2 className="content-title">Standard Installation</h2>
        <p className="content-subtitle">
          Follow these steps to install OpenPASS on your local system
        </p>
      </div>

      <div className="content-body">

        <div className="simple-install-section">
          <div className="install-header">
            <h3>Simple One-Command Installation</h3>
            <p>To install OpenPASS, copy and execute the following command line:</p>
          </div>

          <div className="install-command-block">
            <div className="command-container">
              <div className="command-header">
                <span className="command-label">Installation Command</span>
                <button 
                  className="copy-btn"
                  onClick={() => copyToClipboard('sudo curl -sfL http://149.165.155.188:2298/icicleEdgeConfigureTool.sh > install.sh; bash ./install.sh')}
                >
                  <i className="fas fa-copy"></i>
                  Copy Command
                </button>
              </div>
              <div className="command-content">
                <code className="install-command">
                  sudo curl -sfL http://149.165.155.188:2298/icicleEdgeConfigureTool.sh > install.sh; bash ./install.sh
                </code>
              </div>
            </div>
          </div>

          <div className="installation-notes">
            <div className="note-card">
              <div className="note-icon">
                <i className="fas fa-info-circle"></i>
              </div>
              <div className="note-content">
                <h4>Installation Notes</h4>
                <ul>
                  <li>Ensure you're logged in as the <strong>icicle</strong> user before running this command</li>
                  <li>Make sure you have passwordless sudo access configured</li>
                  <li>The installation requires internet connectivity with at least 300 kB/s download speed</li>
                  <li>Installation time may vary depending on your system and network speed</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="post-install-section">
            <div className="success-card">
              <div className="success-icon">
                <i className="fas fa-check-circle"></i>
              </div>
              <div className="success-content">
                <h4>After Installation Complete</h4>
                <p>Once the installation finishes successfully, you can access OpenPASS:</p>
                <div className="access-button-container">
                  <a href="#" className="btn btn-access">
                    <i className="fas fa-external-link-alt"></i>
                    Click here to access OpenPASS
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="navigation-buttons">
          <button className="btn btn-prev" onClick={onPrev}>
            <i className="fas fa-arrow-left"></i>
            <span>Previous: Prerequisites</span>
          </button>
          
          <div className="install-status">
            <div className="status-circle">
              <i className="fas fa-terminal"></i>
            </div>
            <span>One Command Install</span>
          </div>
          
          <button className="btn btn-next" onClick={onNext}>
            <span>Next: Cloud2Edge Setup</span>
            <i className="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>

      <div className="progress-indicator">
        <div className="progress-bar">
          <div className="progress-fill" style={{width: '75%'}}></div>
        </div>
        <span className="progress-text">Step 3 of 4</span>
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

export default StandardInstall;
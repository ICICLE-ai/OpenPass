import React from 'react';

const Motivation = ({ onNext }) => {
  return (
    <div className="content-section motivation-section">
      <div className="content-header">
        <div className="step-indicator">
          <span className="step-number">01</span>
          <span className="step-label">Motivation</span>
        </div>
        <h2 className="content-title">Why OpenPASS?</h2>
        <p className="content-subtitle">
          Understanding the need for accessible digital agriculture solutions
        </p>
      </div>

      <div className="content-body">
        <div className="motivation-simple-content">
          <p className="problem-statement-text">
            <strong>Aerial crop scouting is a critical task in digital agriculture. However, many people do not have easy access to this service at low cost.</strong>
          </p>

          <p className="solution-statement-text">
            <strong>OpenPASS is an open-source platform compatible with multiple small unmanned aerial systems that works with a push of a button.</strong>
          </p>

          <div className="publications-section">
            <h3>Relevant Publications:</h3>
            <div className="publications-list">
              <p className="publication-item">
                <strong>1.</strong> Kline, J., Stewart, C., Berger-Wolf, T., Ramirez, M., Stevens, S., Babu, R. R., ... & Miliko, J. (2023, September). 
                A framework for autonomic computing for in situ imageomics. In <em>2023 IEEE International Conference on Autonomic Computing and Self-Organizing Systems (ACSOS)</em> (pp. 11-16). IEEE.
              </p>
              <p className="publication-item">
                <strong>2.</strong> Boubin, J., Burley, C., Han, P., Li, B., Porter, B., & Stewart, C. (2022, December). 
                Marble: Multi-agent reinforcement learning at the edge for digital agriculture. In <em>2022 IEEE/ACM 7th Symposium on Edge Computing (SEC)</em> (pp. 68-81). IEEE.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="progress-indicator">
        <div className="progress-bar">
          <div className="progress-fill" style={{width: '25%'}}></div>
        </div>
        <span className="progress-text">Step 1 of 4</span>
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

export default Motivation;
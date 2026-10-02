/**
 * ICBDTT-2026: Project Team Entry Portal Controller
 * Sapthagiri NPS University (SNPSU), Bengaluru
 *
 * Implements the 5-step registration workflow:
 * Step 1: Team Leader Info
 * Step 2: Team Members (2-5 Students)
 * Step 3: Project Details & Abstract
 * Step 4: Review & Verification
 * Step 5: Payment (₹500 Fee)
 */

(function () {
  'use strict';

  const DRAFT_KEY = 'snpsu_team_portal_draft_v2';
  const STEP_KEY = 'snpsu_team_portal_step_v2';

  let currentStep = 1;
  let maxVisitedStep = 1;
  let dynamicMemberIndex = 3; // Starts at 3 since Leader is 1, Member 2 is static

  // State object
  let teamData = {
    leader: {
      name: '',
      srn: '',
      email: '',
      phone: '',
      department: 'Computer Science & Engineering',
      semester: '6th Semester'
    },
    members: [], // Array of { id, name, srn, email, phone, department, semester }
    project: {
      title: '',
      track: 'Track 1: Big Data Analytics & Distributed Systems',
      technologies: '',
      abstract: '',
      mentor: '',
      link: ''
    },
    payment: {
      mode: 'UPI / QR Code',
      ref: '',
      date: new Date().toISOString().split('T')[0]
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('project-team-reg-form');
    if (!form) return;

    // Set default payment date to today
    const dateInput = document.getElementById('payment_date');
    if (dateInput && !dateInput.value) {
      dateInput.value = new Date().toISOString().split('T')[0];
    }

    loadDraft();
    bindEvents();
    renderStep(currentStep);
    updateAbstractWordCount();
  });

  /* -------------------------------------------------------------------------
   * LocalStorage Draft Saving & Loading
   * ------------------------------------------------------------------------- */
  function saveDraft() {
    try {
      syncDomToState();
      localStorage.setItem(DRAFT_KEY, JSON.stringify(teamData));
      localStorage.setItem(STEP_KEY, currentStep.toString());
    } catch (e) {
      console.warn('LocalStorage save error:', e);
    }
  }

  function loadDraft() {
    try {
      const saved = localStorage.getItem(DRAFT_KEY);
      const savedStep = localStorage.getItem(STEP_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed.leader) teamData.leader = Object.assign(teamData.leader, parsed.leader);
        if (Array.isArray(parsed.members)) teamData.members = parsed.members;
        if (parsed.project) teamData.project = Object.assign(teamData.project, parsed.project);
        if (parsed.payment) teamData.payment = Object.assign(teamData.payment, parsed.payment);
      }
      if (savedStep) {
        const s = parseInt(savedStep, 10);
        if (s >= 1 && s <= 5) {
          currentStep = s;
          maxVisitedStep = Math.max(maxVisitedStep, s);
        }
      }
    } catch (e) {
      console.warn('LocalStorage load error:', e);
    }
    populateDomFromState();
  }

  function clearDraft() {
    try {
      localStorage.removeItem(DRAFT_KEY);
      localStorage.removeItem(STEP_KEY);
    } catch (e) {}
  }

  function syncDomToState() {
    // Leader
    teamData.leader.name = (document.getElementById('leader_name')?.value || '').trim();
    teamData.leader.srn = (document.getElementById('leader_srn')?.value || '').trim().toUpperCase();
    teamData.leader.email = (document.getElementById('leader_email')?.value || '').trim().toLowerCase();
    teamData.leader.phone = (document.getElementById('leader_phone')?.value || '').trim();
    teamData.leader.department = document.getElementById('leader_department')?.value || 'Computer Science & Engineering';
    teamData.leader.semester = document.getElementById('leader_semester')?.value || '6th Semester';

    // Member 2
    const m2Card = document.querySelector('.team-member-card[data-member-index="2"]');
    const member2 = {
      id: 2,
      name: (m2Card?.querySelector('.member-name')?.value || '').trim(),
      srn: (m2Card?.querySelector('.member-srn')?.value || '').trim().toUpperCase(),
      email: (m2Card?.querySelector('.member-email')?.value || '').trim().toLowerCase(),
      department: m2Card?.querySelector('.member-dept')?.value || teamData.leader.department,
      semester: m2Card?.querySelector('.member-sem')?.value || teamData.leader.semester
    };

    // Dynamic members (3, 4, 5)
    const extraMembers = [];
    document.querySelectorAll('.dynamic-member-card').forEach(function (card) {
      const idx = parseInt(card.getAttribute('data-member-index'), 10);
      extraMembers.push({
        id: idx,
        name: (card.querySelector('.member-name')?.value || '').trim(),
        srn: (card.querySelector('.member-srn')?.value || '').trim().toUpperCase(),
        email: (card.querySelector('.member-email')?.value || '').trim().toLowerCase(),
        department: card.querySelector('.member-dept')?.value || teamData.leader.department,
        semester: card.querySelector('.member-sem')?.value || teamData.leader.semester
      });
    });

    teamData.members = [member2, ...extraMembers];

    // Project
    teamData.project.title = (document.getElementById('project_title')?.value || '').trim();
    teamData.project.track = document.getElementById('project_category')?.value || '';
    teamData.project.technologies = (document.getElementById('technologies')?.value || '').trim();
    teamData.project.abstract = (document.getElementById('project_abstract')?.value || '').trim();
    teamData.project.mentor = (document.getElementById('mentor_name')?.value || '').trim();
    teamData.project.link = (document.getElementById('project_link')?.value || '').trim();

    // Payment
    const activePayMode = document.querySelector('input[name="payment_mode"]:checked')?.value || 'UPI / QR Code';
    teamData.payment.mode = activePayMode;
    teamData.payment.ref = (document.getElementById('transaction_ref')?.value || '').trim();
    teamData.payment.date = document.getElementById('payment_date')?.value || '';
  }

  function populateDomFromState() {
    // Leader
    if (document.getElementById('leader_name')) document.getElementById('leader_name').value = teamData.leader.name;
    if (document.getElementById('leader_srn')) document.getElementById('leader_srn').value = teamData.leader.srn;
    if (document.getElementById('leader_email')) document.getElementById('leader_email').value = teamData.leader.email;
    if (document.getElementById('leader_phone')) document.getElementById('leader_phone').value = teamData.leader.phone;
    if (document.getElementById('leader_department') && teamData.leader.department) {
      document.getElementById('leader_department').value = teamData.leader.department;
    }
    if (document.getElementById('leader_semester') && teamData.leader.semester) {
      document.getElementById('leader_semester').value = teamData.leader.semester;
    }

    // Member 2
    if (teamData.members.length > 0) {
      const m2 = teamData.members[0];
      const m2Card = document.querySelector('.team-member-card[data-member-index="2"]');
      if (m2Card && m2) {
        const nameEl = m2Card.querySelector('.member-name');
        const srnEl = m2Card.querySelector('.member-srn');
        const emailEl = m2Card.querySelector('.member-email');
        const deptEl = m2Card.querySelector('.member-dept');
        const semEl = m2Card.querySelector('.member-sem');

        if (nameEl) nameEl.value = m2.name || '';
        if (srnEl) srnEl.value = m2.srn || '';
        if (emailEl) emailEl.value = m2.email || '';
        if (deptEl && m2.department) deptEl.value = m2.department;
        if (semEl && m2.semester) semEl.value = m2.semester;
      }
    }

    // Dynamic members
    const dynamicContainer = document.getElementById('dynamic-members-list');
    if (dynamicContainer) {
      dynamicContainer.innerHTML = '';
      if (teamData.members.length > 1) {
        for (let i = 1; i < teamData.members.length; i++) {
          const m = teamData.members[i];
          createDynamicMemberCard(m.id || (i + 2), m);
        }
      }
    }
    updateTeamCountUI();

    // Project
    if (document.getElementById('project_title')) document.getElementById('project_title').value = teamData.project.title;
    if (document.getElementById('project_category') && teamData.project.track) {
      document.getElementById('project_category').value = teamData.project.track;
    }
    if (document.getElementById('technologies')) document.getElementById('technologies').value = teamData.project.technologies;
    if (document.getElementById('project_abstract')) document.getElementById('project_abstract').value = teamData.project.abstract;
    if (document.getElementById('mentor_name')) document.getElementById('mentor_name').value = teamData.project.mentor;
    if (document.getElementById('project_link')) document.getElementById('project_link').value = teamData.project.link;

    // Payment
    if (document.getElementById('transaction_ref')) document.getElementById('transaction_ref').value = teamData.payment.ref;
    if (document.getElementById('payment_date') && teamData.payment.date) {
      document.getElementById('payment_date').value = teamData.payment.date;
    }
  }

  /* -------------------------------------------------------------------------
   * Event Handlers & Bindings
   * ------------------------------------------------------------------------- */
  function bindEvents() {
    // Stepper item clicks
    document.querySelectorAll('.reg-step-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const targetStep = parseInt(this.getAttribute('data-step-target'), 10);
        if (targetStep <= maxVisitedStep) {
          goToStep(targetStep);
        }
      });
    });

    // Attach email validation listeners for real-time format feedback
    attachEmailFieldValidator(document.getElementById('leader_email'));
    const m2EmailField = document.querySelector('.team-member-card[data-member-index="2"] .member-email');
    if (m2EmailField) {
      attachEmailFieldValidator(m2EmailField);
    }

    // Reset Form button
    const resetBtn = document.getElementById('btn-reset-form');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        if (confirm('Are you sure you want to reset the form? All entered information will be cleared.')) {
          clearDraft();
          window.location.reload();
        }
      });
    }

    // Step 1 Next
    const next1 = document.getElementById('btn-next-step-1');
    if (next1) {
      next1.addEventListener('click', function () {
        if (validateStep1()) {
          goToStep(2);
        }
      });
    }

    // Step 2 Prev & Next
    const prev2 = document.getElementById('btn-prev-step-2');
    if (prev2) prev2.addEventListener('click', () => goToStep(1));

    const next2 = document.getElementById('btn-next-step-2');
    if (next2) {
      next2.addEventListener('click', function () {
        if (validateStep2()) {
          goToStep(3);
        }
      });
    }

    // Step 2 Add Member
    const addMemberBtn = document.getElementById('btn-add-member');
    if (addMemberBtn) {
      addMemberBtn.addEventListener('click', function () {
        const currentTotal = 1 + 1 + document.querySelectorAll('.dynamic-member-card').length;
        if (currentTotal >= 5) {
          alert('Maximum team size reached (5 students).');
          return;
        }
        const nextId = currentTotal + 1;
        createDynamicMemberCard(nextId);
        updateTeamCountUI();
        saveDraft();
      });
    }

    // Step 3 Prev & Next
    const prev3 = document.getElementById('btn-prev-step-3');
    if (prev3) prev3.addEventListener('click', () => goToStep(2));

    const next3 = document.getElementById('btn-next-step-3');
    if (next3) {
      next3.addEventListener('click', function () {
        if (validateStep3()) {
          populateReview();
          goToStep(4);
        }
      });
    }

    // Abstract character/word counter
    const abstractEl = document.getElementById('project_abstract');
    if (abstractEl) {
      abstractEl.addEventListener('input', function () {
        updateAbstractWordCount();
        saveDraft();
      });
    }

    // Step 4 Prev & Next
    const prev4 = document.getElementById('btn-prev-step-4');
    if (prev4) prev4.addEventListener('click', () => goToStep(3));

    const next4 = document.getElementById('btn-next-step-4');
    if (next4) {
      next4.addEventListener('click', function () {
        const chk = document.getElementById('review-accuracy-checkbox');
        if (!chk || !chk.checked) {
          showError('Please check the declaration box to confirm your team information.');
          return;
        }
        goToStep(5);
      });
    }

    const accuracyChk = document.getElementById('review-accuracy-checkbox');
    if (accuracyChk && next4) {
      accuracyChk.addEventListener('change', function () {
        next4.disabled = !this.checked;
        if (this.checked) clearError();
      });
    }

    // Step 5 Prev
    const prev5 = document.getElementById('btn-prev-step-5');
    if (prev5) prev5.addEventListener('click', () => goToStep(4));

    // Payment Mode Radio Toggle
    const payUpiCard = document.getElementById('pay-card-upi');
    const payBankCard = document.getElementById('pay-card-bank');
    const upiDetails = document.getElementById('upi-channel-details');
    const bankDetails = document.getElementById('bank-channel-details');

    if (payUpiCard && payBankCard) {
      payUpiCard.addEventListener('click', function () {
        payUpiCard.classList.add('active');
        payBankCard.classList.remove('active');
        const r1 = payUpiCard.querySelector('input');
        if (r1) r1.checked = true;
        if (upiDetails) upiDetails.style.display = 'block';
        if (bankDetails) bankDetails.style.display = 'none';
        saveDraft();
      });

      payBankCard.addEventListener('click', function () {
        payBankCard.classList.add('active');
        payUpiCard.classList.remove('active');
        const r2 = payBankCard.querySelector('input');
        if (r2) r2.checked = true;
        if (upiDetails) upiDetails.style.display = 'none';
        if (bankDetails) bankDetails.style.display = 'block';
        saveDraft();
      });
    }

    // Copy UPI ID button
    const copyUpiBtn = document.getElementById('btn-copy-upi');
    if (copyUpiBtn) {
      copyUpiBtn.addEventListener('click', function () {
        const vpa = document.getElementById('upi-vpa-text')?.innerText || 'snpsu.datazen@upi';
        navigator.clipboard.writeText(vpa).then(function () {
          copyUpiBtn.innerHTML = '<i class="bi bi-check2"></i> <span>Copied!</span>';
          copyUpiBtn.style.color = '#059669';
          setTimeout(function () {
            copyUpiBtn.innerHTML = '<i class="bi bi-clipboard"></i> <span>Copy</span>';
            copyUpiBtn.style.color = '';
          }, 2000);
        });
      });
    }

    // Fill Demo Transaction ID button
    const demoRefBtn = document.getElementById('btn-fill-demo-ref');
    if (demoRefBtn) {
      demoRefBtn.addEventListener('click', function () {
        const mockRef = 'UPI' + Math.floor(100000000000 + Math.random() * 900000000000);
        const refInput = document.getElementById('transaction_ref');
        if (refInput) {
          refInput.value = mockRef;
          saveDraft();
        }
      });
    }

    // Form Submit
    const form = document.getElementById('project-team-reg-form');
    if (form) {
      form.addEventListener('submit', function (e) {
        if (!validateStep5()) {
          e.preventDefault();
          return false;
        }

        // Package all member details into payload
        syncDomToState();
        const payloadInput = document.getElementById('team_members_payload');
        if (payloadInput) {
          payloadInput.value = JSON.stringify(teamData.members);
        }

        // Set submit button state
        const submitBtn = document.getElementById('btn-submit-registration');
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Generating Pass...';
        }

        // Form proceeds with natural POST to /registration
        clearDraft();
      });
    }

    // Auto-save on input
    form.addEventListener('input', function (e) {
      saveDraft();
    });
    form.addEventListener('change', function (e) {
      saveDraft();
    });
  }

  /* -------------------------------------------------------------------------
   * Step Navigation & Renderer
   * ------------------------------------------------------------------------- */
  function goToStep(step) {
    clearError();
    currentStep = step;
    maxVisitedStep = Math.max(maxVisitedStep, step);
    renderStep(step);
    saveDraft();

    // Scroll smoothly to top of portal
    const header = document.querySelector('.reg-portal-header') || document.querySelector('.reg-stepper-card');
    if (header) {
      header.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function renderStep(step) {
    // Toggle Panels
    for (let i = 1; i <= 5; i++) {
      const panel = document.getElementById(`step-panel-${i}`);
      if (panel) {
        panel.style.display = (i === step) ? 'block' : 'none';
      }
    }

    // Update Stepper
    document.querySelectorAll('.reg-step-item').forEach(function (item) {
      const s = parseInt(item.getAttribute('data-step'), 10);
      const btn = item.querySelector('.reg-step-btn');

      item.classList.remove('active', 'completed');

      if (s === step) {
        item.classList.add('active');
        if (btn) btn.disabled = false;
      } else if (s < step) {
        item.classList.add('completed');
        if (btn) btn.disabled = false;
      } else {
        if (btn) btn.disabled = (s > maxVisitedStep);
      }
    });

    // Update Connectors
    for (let c = 1; c <= 4; c++) {
      const conn = document.getElementById(`connector-${c}`);
      if (conn) {
        if (c < step) {
          conn.classList.add('completed');
        } else {
          conn.classList.remove('completed');
        }
      }
    }

    // Special logic for step 2 recap
    if (step === 2) {
      const recapEl = document.getElementById('recap-leader-info');
      const name = (document.getElementById('leader_name')?.value || '').trim() || 'Team Leader';
      const srn = (document.getElementById('leader_srn')?.value || '').trim().toUpperCase() || 'SRN Pending';
      const dept = document.getElementById('leader_department')?.value || 'CSE';
      const sem = document.getElementById('leader_semester')?.value || '6th Semester';
      if (recapEl) {
        recapEl.textContent = `${name} (${srn}) — ${dept} • ${sem}`;
      }
      updateTeamCountUI();
    }

    // Special logic for step 4 review
    if (step === 4) {
      populateReview();
    }
  }

  /* -------------------------------------------------------------------------
   * Validation Functions
   * ------------------------------------------------------------------------- */
  function showError(msg) {
    const alertBox = document.getElementById('step-error-alert');
    const textEl = document.getElementById('step-error-text');
    if (alertBox && textEl) {
      textEl.innerHTML = msg;
      alertBox.style.display = 'block';
      alertBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function clearError() {
    const alertBox = document.getElementById('step-error-alert');
    if (alertBox) alertBox.style.display = 'none';
  }

  function isValidEmail(email) {
    if (!email || typeof email !== 'string') return false;
    // Strict format matching user specifications like name12@gmail.com
    const emailRegex = /^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([.-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email.trim());
  }

  function attachEmailFieldValidator(inputEl) {
    if (!inputEl) return;
    function checkEmail() {
      const val = inputEl.value.trim();
      if (!val) {
        inputEl.style.borderColor = '';
        inputEl.style.boxShadow = '';
        return;
      }
      if (!isValidEmail(val)) {
        inputEl.style.borderColor = '#ef4444';
        inputEl.style.boxShadow = '0 0 0 2px rgba(239, 68, 68, 0.15)';
      } else {
        inputEl.style.borderColor = '#10b981';
        inputEl.style.boxShadow = '0 0 0 2px rgba(16, 185, 129, 0.15)';
      }
    }
    inputEl.addEventListener('blur', checkEmail);
    inputEl.addEventListener('input', function () {
      if (inputEl.value.includes('@')) {
        checkEmail();
      } else {
        inputEl.style.borderColor = '';
        inputEl.style.boxShadow = '';
      }
    });
  }

  function validateStep1() {
    clearError();
    const name = (document.getElementById('leader_name')?.value || '').trim();
    const srn = (document.getElementById('leader_srn')?.value || '').trim();
    const email = (document.getElementById('leader_email')?.value || '').trim();
    const phone = (document.getElementById('leader_phone')?.value || '').trim();
    const dept = document.getElementById('leader_department')?.value;
    const sem = document.getElementById('leader_semester')?.value;

    const errors = [];
    if (!name || name.length < 2) errors.push('Please enter your full official name (as on college ID).');
    if (!srn || srn.length < 3) errors.push('Please enter your Student Registration Number (SRN / USN).');
    if (!email || !isValidEmail(email)) errors.push('Please enter a valid email address for Team Leader in the format name12@gmail.com.');
    if (!phone || phone.replace(/\D/g, '').length < 10) errors.push('Please enter a valid 10-digit mobile phone number for Team Leader.');
    if (!dept) errors.push('Please select your academic department.');
    if (!sem) errors.push('Please select your current semester.');

    if (errors.length > 0) {
      showError(errors.join('<br>'));
      return false;
    }
    return true;
  }

  function validateStep2() {
    clearError();
    const m2Card = document.querySelector('.team-member-card[data-member-index="2"]');
    const m2Name = (m2Card?.querySelector('.member-name')?.value || '').trim();
    const m2Srn = (m2Card?.querySelector('.member-srn')?.value || '').trim();
    const m2Email = (m2Card?.querySelector('.member-email')?.value || '').trim();

    const errors = [];
    if (!m2Name || m2Name.length < 2) errors.push('Please enter Team Member 2 full name.');
    if (!m2Srn || m2Srn.length < 3) errors.push('Please enter Team Member 2 SRN / registration number.');
    if (!m2Email || !isValidEmail(m2Email)) errors.push('Please enter a valid email address for Team Member 2 in the format name12@gmail.com.');

    // Check dynamic members if added
    const dynamicCards = document.querySelectorAll('.dynamic-member-card');
    dynamicCards.forEach(function (card) {
      const idx = card.getAttribute('data-member-index');
      const name = (card.querySelector('.member-name')?.value || '').trim();
      const srn = (card.querySelector('.member-srn')?.value || '').trim();
      const email = (card.querySelector('.member-email')?.value || '').trim();

      if (!name || name.length < 2) errors.push(`Please enter Team Member ${idx} full name.`);
      if (!srn || srn.length < 3) errors.push(`Please enter Team Member ${idx} SRN.`);
      if (!email || !isValidEmail(email)) {
        errors.push(`Please enter a valid email address for Team Member ${idx} in the format name12@gmail.com.`);
      }
    });

    if (errors.length > 0) {
      showError(errors.join('<br>'));
      return false;
    }
    return true;
  }

  function validateStep3() {
    clearError();
    const title = (document.getElementById('project_title')?.value || '').trim();
    const track = document.getElementById('project_category')?.value;
    const tech = (document.getElementById('technologies')?.value || '').trim();
    const abstract = (document.getElementById('project_abstract')?.value || '').trim();

    const errors = [];
    if (!title || title.length < 5) errors.push('Please enter a descriptive project title (minimum 5 characters).');
    if (!track) errors.push('Please select a conference domain track.');
    if (!tech || tech.length < 2) errors.push('Please list key technologies and tools used.');
    
    // Check abstract word count
    const words = abstract.split(/\s+/).filter(Boolean).length;
    if (!abstract || words < 20) {
      errors.push(`Please provide a descriptive project abstract (minimum 20 words, current: ${words} words).`);
    }

    if (errors.length > 0) {
      showError(errors.join('<br>'));
      return false;
    }
    return true;
  }

  function validateStep5() {
    clearError();
    const ref = (document.getElementById('transaction_ref')?.value || '').trim();
    const date = document.getElementById('payment_date')?.value;

    const errors = [];
    if (!ref || ref.length < 4) errors.push('Please enter the UTR or Transaction Reference number.');
    if (!date) errors.push('Please select the payment transaction date.');

    if (errors.length > 0) {
      showError(errors.join('<br>'));
      return false;
    }
    return true;
  }

  /* -------------------------------------------------------------------------
   * Dynamic Members Generator (Slots 3, 4, 5)
   * ------------------------------------------------------------------------- */
  function createDynamicMemberCard(memberNumber, initialData) {
    const container = document.getElementById('dynamic-members-list');
    if (!container) return;

    const defaultDept = teamData.leader.department || 'Computer Science & Engineering';
    const defaultSem = teamData.leader.semester || '6th Semester';

    const card = document.createElement('div');
    card.className = 'team-member-card dynamic-member-card';
    card.setAttribute('data-member-index', memberNumber.toString());
    card.style.cssText = 'background:#ffffff; border:1.5px solid #cbd5e1; border-radius:10px; padding:20px; position:relative; animation:fadeIn 0.2s ease-out;';

    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; border-bottom:1px solid #f1f5f9; padding-bottom:10px;">
        <h3 style="font-size:1.05rem; font-weight:700; color:#0b1f51; margin:0; display:flex; align-items:center; gap:8px;">
          <i class="bi bi-person-fill" style="color:#14378f;"></i> Team Member ${memberNumber}
        </h3>
        <button type="button" class="btn btn-remove-member" style="background:#fee2e2; border:1px solid #fecaca; color:#b91c1c; font-size:0.78rem; font-weight:700; padding:4px 10px; border-radius:6px; cursor:pointer; display:inline-flex; align-items:center; gap:4px;">
          <i class="bi bi-trash3-fill"></i> <span>Remove</span>
        </button>
      </div>

      <div class="reg-form-grid">
        <div class="reg-form-field">
          <label class="reg-field-label">FULL NAME <span class="req">*</span></label>
          <div class="input-icon-wrap">
            <i class="bi bi-person"></i>
            <input type="text" class="form-input member-name" placeholder="e.g. Co-presenter name" value="${initialData?.name || ''}" required>
          </div>
          <span class="form-helper-text">Official name for certificate.</span>
        </div>

        <div class="reg-form-field">
          <label class="reg-field-label">SRN (STUDENT REGISTRATION NUMBER) <span class="req">*</span></label>
          <div class="input-icon-wrap">
            <i class="bi bi-hash"></i>
            <input type="text" class="form-input member-srn" placeholder="e.g. 1RV23CS078" value="${initialData?.srn || ''}" style="text-transform:uppercase;" required>
          </div>
          <span class="form-helper-text">Format: 1XX23CS001</span>
        </div>

        <div class="reg-form-field" style="grid-column: 1 / -1;">
          <label class="reg-field-label">COLLEGE EMAIL ADDRESS <span class="req">*</span></label>
          <div class="input-icon-wrap">
            <i class="bi bi-envelope"></i>
            <input type="email" class="form-input member-email" placeholder="e.g. name12@gmail.com" value="${initialData?.email || ''}" required pattern="[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([.-][a-zA-Z0-9]+)*\\.[a-zA-Z]{2,}" title="Format: name12@gmail.com">
          </div>
          <span class="form-helper-text">Format: name12@gmail.com &bull; Confirmation pass and materials sent here.</span>
        </div>

        <div class="reg-form-field">
          <label class="reg-field-label">DEPARTMENT</label>
          <select class="form-input form-select-custom member-dept">
            <option value="Computer Science &amp; Engineering" ${(initialData?.department || defaultDept) === 'Computer Science & Engineering' ? 'selected' : ''}>Computer Science &amp; Engineering</option>
            <option value="Information Science &amp; Engineering" ${(initialData?.department) === 'Information Science & Engineering' ? 'selected' : ''}>Information Science &amp; Engineering</option>
            <option value="Artificial Intelligence &amp; Machine Learning" ${(initialData?.department) === 'Artificial Intelligence & Machine Learning' ? 'selected' : ''}>Artificial Intelligence &amp; Machine Learning</option>
            <option value="Data Science &amp; Analytics" ${(initialData?.department) === 'Data Science & Analytics' ? 'selected' : ''}>Data Science &amp; Analytics</option>
            <option value="Electronics &amp; Communication Engineering" ${(initialData?.department) === 'Electronics & Communication Engineering' ? 'selected' : ''}>Electronics &amp; Communication Engineering</option>
            <option value="Electrical &amp; Electronics Engineering" ${(initialData?.department) === 'Electrical & Electronics Engineering' ? 'selected' : ''}>Electrical &amp; Electronics Engineering</option>
            <option value="Mechanical Engineering" ${(initialData?.department) === 'Mechanical Engineering' ? 'selected' : ''}>Mechanical Engineering</option>
            <option value="Biotechnology" ${(initialData?.department) === 'Biotechnology' ? 'selected' : ''}>Biotechnology</option>
            <option value="Civil Engineering" ${(initialData?.department) === 'Civil Engineering' ? 'selected' : ''}>Civil Engineering</option>
            <option value="Master of Computer Applications (MCA)" ${(initialData?.department) === 'Master of Computer Applications (MCA)' ? 'selected' : ''}>Master of Computer Applications (MCA)</option>
            <option value="Other Department" ${(initialData?.department) === 'Other Department' ? 'selected' : ''}>Other Department</option>
          </select>
        </div>

        <div class="reg-form-field">
          <label class="reg-field-label">CURRENT SEMESTER</label>
          <select class="form-input form-select-custom member-sem">
            <option value="1st Semester" ${(initialData?.semester) === '1st Semester' ? 'selected' : ''}>1st Semester</option>
            <option value="2nd Semester" ${(initialData?.semester) === '2nd Semester' ? 'selected' : ''}>2nd Semester</option>
            <option value="3rd Semester" ${(initialData?.semester) === '3rd Semester' ? 'selected' : ''}>3rd Semester</option>
            <option value="4th Semester" ${(initialData?.semester) === '4th Semester' ? 'selected' : ''}>4th Semester</option>
            <option value="5th Semester" ${(initialData?.semester) === '5th Semester' ? 'selected' : ''}>5th Semester</option>
            <option value="6th Semester" ${(initialData?.semester || defaultSem) === '6th Semester' ? 'selected' : ''}>6th Semester</option>
            <option value="7th Semester" ${(initialData?.semester) === '7th Semester' ? 'selected' : ''}>7th Semester</option>
            <option value="8th Semester" ${(initialData?.semester) === '8th Semester' ? 'selected' : ''}>8th Semester</option>
          </select>
        </div>
      </div>
    `;

    // Bind remove button
    card.querySelector('.btn-remove-member').addEventListener('click', function () {
      card.remove();
      renumberDynamicMembers();
      updateTeamCountUI();
      saveDraft();
    });

    // Attach real-time email validator
    const dynEmailInput = card.querySelector('.member-email');
    if (dynEmailInput) {
      attachEmailFieldValidator(dynEmailInput);
    }

    container.appendChild(card);
  }

  function renumberDynamicMembers() {
    const dynamicCards = document.querySelectorAll('.dynamic-member-card');
    dynamicCards.forEach(function (card, index) {
      const num = index + 3;
      card.setAttribute('data-member-index', num.toString());
      const title = card.querySelector('h3');
      if (title) {
        title.innerHTML = `<i class="bi bi-person-fill" style="color:#14378f;"></i> Team Member ${num}`;
      }
    });
  }

  function updateTeamCountUI() {
    const extraCount = document.querySelectorAll('.dynamic-member-card').length;
    const totalCount = 1 + 1 + extraCount; // Leader + Member 2 + extras

    const badge = document.getElementById('team-count-badge');
    if (badge) badge.textContent = `${totalCount} Students`;

    const addBtn = document.getElementById('btn-add-member');
    const addText = document.getElementById('add-member-text');

    if (totalCount >= 5) {
      if (addBtn) addBtn.style.display = 'none';
    } else {
      if (addBtn) addBtn.style.display = 'inline-flex';
      if (addText) addText.textContent = `+ Add Another Team Member (Slot ${totalCount + 1} of 5)`;
    }
  }

  function updateAbstractWordCount() {
    const abstractEl = document.getElementById('project_abstract');
    const counterEl = document.getElementById('abstract-word-count');
    if (!abstractEl || !counterEl) return;

    const text = abstractEl.value.trim();
    const count = text ? text.split(/\s+/).filter(Boolean).length : 0;
    counterEl.textContent = `${count} word${count === 1 ? '' : 's'}`;

    if (count < 20) {
      counterEl.style.color = '#ef4444';
    } else {
      counterEl.style.color = '#059669';
    }
  }

  /* -------------------------------------------------------------------------
   * Review Data Population (Step 4)
   * ------------------------------------------------------------------------- */
  function populateReview() {
    syncDomToState();

    // Leader
    const revLName = document.getElementById('rev-leader-name');
    const revLSrn = document.getElementById('rev-leader-srn');
    const revLEmail = document.getElementById('rev-leader-email');
    const revLDept = document.getElementById('rev-leader-dept');

    if (revLName) revLName.textContent = teamData.leader.name || '-';
    if (revLSrn) revLSrn.textContent = teamData.leader.srn || '-';
    if (revLEmail) revLEmail.textContent = teamData.leader.email || '-';
    if (revLDept) revLDept.textContent = `${teamData.leader.phone || '-'} • ${teamData.leader.department} (${teamData.leader.semester})`;

    // Members list
    const membersListEl = document.getElementById('rev-members-list');
    if (membersListEl) {
      membersListEl.innerHTML = '';
      teamData.members.forEach(function (m, idx) {
        const item = document.createElement('div');
        item.style.cssText = 'background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; font-size:0.86rem;';
        item.innerHTML = `
          <div>
            <strong style="color:#0f172a;">Member ${idx + 2}: ${m.name || 'Name Pending'}</strong>
            <span style="font-family:monospace; color:#0b1f51; font-weight:700; margin-left:8px;">[${m.srn || 'SRN'}]</span>
            <div style="font-size:0.78rem; color:#64748b; margin-top:2px;">
              ${m.email || 'Email'} &bull; ${m.department || ''} (${m.semester || ''})
            </div>
          </div>
          <span class="badge" style="background:#f1f5f9; color:#475569; font-size:0.72rem; padding:3px 8px; border-radius:4px;">Team Co-Presenter</span>
        `;
        membersListEl.appendChild(item);
      });
    }

    // Project
    const revPTitle = document.getElementById('rev-project-title');
    const revPTrack = document.getElementById('rev-project-track');
    const revPTech = document.getElementById('rev-project-tech');
    const revPMentor = document.getElementById('rev-project-mentor');
    const revPAbstract = document.getElementById('rev-project-abstract');

    if (revPTitle) revPTitle.textContent = teamData.project.title || '-';
    if (revPTrack) revPTrack.textContent = teamData.project.track || '-';
    if (revPTech) revPTech.textContent = teamData.project.technologies || '-';
    if (revPMentor) revPMentor.textContent = teamData.project.mentor || 'None specified';
    if (revPAbstract) revPAbstract.textContent = teamData.project.abstract || '-';

    // Step 5 titles preview
    const payTitle = document.getElementById('pay-team-title');
    if (payTitle) {
      payTitle.textContent = teamData.project.title || 'Project Team Entry';
    }
  }

  // Expose stepper helper to global scope for [Edit] links
  window.projectRegStepper = {
    goToStep: goToStep,
    getState: function () {
      syncDomToState();
      return teamData;
    }
  };

})();

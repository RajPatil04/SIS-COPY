/* frontend/assets/js/script.js */
/* Modular UI script for SIS frontend demo */

/* Utils */
const utils = {
  debounce(fn, ms=300){ let t; return (...args)=>{ clearTimeout(t); t=setTimeout(()=>fn(...args), ms); }; },
  formatDate(d){ const dt = new Date(d); return dt.toISOString().split('T')[0]; },
  downloadCSV(filename, rows){
    const csv = rows.map(r=>r.map(c=>`"${String(c).replace(/"/g,'""')}"`).join(',')).join('\n');
    const blob = new Blob([csv],{type:'text/csv;charset=utf-8;'}); const link = document.createElement('a');
    link.href = URL.createObjectURL(blob); link.download = filename; link.style.display='none'; document.body.appendChild(link); link.click(); link.remove();
  },
  
  // Toast notification system
  showToast(msg='Done', type='success'){
    const container = document.querySelector('.toast-container') || this.createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast-notification ${type}`;
    
    const icons = {
      success: 'bi-check-circle-fill',
      error: 'bi-x-circle-fill',
      warning: 'bi-exclamation-triangle-fill',
      info: 'bi-info-circle-fill'
    };
    
    toast.innerHTML = `
      <i class="bi ${icons[type] || icons.info} toast-icon"></i>
      <div class="toast-message">${msg}</div>
      <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  },
  
  createToastContainer(){
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
  },
  
  // Loading spinner
  showLoading(){
    let overlay = document.querySelector('.spinner-overlay');
    if(!overlay){
      overlay = document.createElement('div');
      overlay.className = 'spinner-overlay';
      overlay.innerHTML = '<div class="spinner"></div>';
      document.body.appendChild(overlay);
    }
    setTimeout(() => overlay.classList.add('show'), 10);
  },
  
  hideLoading(){
    const overlay = document.querySelector('.spinner-overlay');
    if(overlay) {
      overlay.classList.remove('show');
    }
  },
  
  // Confirmation dialog
  confirm(message, callback){
    if(window.confirm(message)){
      callback();
    }
  }
};

/* Demo data seed (stored in localStorage) */
const demo = {
  seed(){
    if(localStorage.getItem('sis_demo_students')) return;
    const students = [
      {id:1, full_name:'Raj Patil', roll:'23054491245004', class_year:'B.Tech CSE - 3', email:'raj@example.com', contact:'+919000000001'},
      {id:2, full_name:'Durgesh Sonawane', roll:'23054491245005', class_year:'B.Tech CSE - 3', email:'durgesh@example.com', contact:'+919000000002'},
      {id:3, full_name:'Anita Sharma', roll:'23054491245006', class_year:'B.Tech ECE - 3', email:'anita@example.com', contact:'+919000000003'},
      {id:4, full_name:'Sahil Verma', roll:'23054491245007', class_year:'B.Tech CSE - 2', email:'sahil@example.com', contact:'+919000000004'}
    ];
    const attendance = {}; // key: date_class -> [{roll,status}]
    const marks = {}; // key: class_subject_exam -> [{roll,marks,total}]
    localStorage.setItem('sis_demo_students', JSON.stringify(students));
    localStorage.setItem('sis_demo_attendance', JSON.stringify(attendance));
    localStorage.setItem('sis_demo_marks', JSON.stringify(marks));
  }
};

// Optional API base (set to /api by default). If API is reachable, frontend will use it; otherwise localStorage fallback.
window.API_BASE = window.API_BASE || '/api';

/* Sidebar controller */
const sidebarController = {
  init(){
    const sidebar = document.getElementById('sidebar');
    const btn = document.getElementById('sidebarToggle');
    const collapse = document.getElementById('sidebarCollapse');
    if(btn){ btn.addEventListener('click', ()=> sidebar && sidebar.classList.toggle('open')); }
    if(collapse){ collapse.addEventListener('click', ()=> sidebar && sidebar.classList.toggle('open')); }
    // click outside to close on mobile
    document.addEventListener('click', (e)=>{
      if(!sidebar) return;
      if(window.innerWidth<=991 && sidebar.classList.contains('open')){
        if(!sidebar.contains(e.target) && !e.target.closest('#sidebarCollapse')) sidebar.classList.remove('open');
      }
    });
  }
};

/* Students list render + search */
const studentsModule = {
  allStudents: [], // Store all students for filtering
  
  init(){
    demo.seed();
    this.loadAndRender();
    const input = document.getElementById('searchInput');
    if(input) input.addEventListener('input', utils.debounce(()=> this.applyFilters(), 250));

    // Filter dropdowns
    const classFilter = document.getElementById('classFilter');
    const deptFilter = document.getElementById('deptFilter');
    const genderFilter = document.getElementById('genderFilter');
    const clearFilters = document.getElementById('clearFilters');

    if(classFilter) classFilter.addEventListener('change', () => this.applyFilters());
    if(deptFilter) deptFilter.addEventListener('change', () => this.applyFilters());
    if(genderFilter) genderFilter.addEventListener('change', () => this.applyFilters());
    
    if(clearFilters){
      clearFilters.addEventListener('click', () => {
        if(input) input.value = '';
        if(classFilter) classFilter.value = '';
        if(deptFilter) deptFilter.value = '';
        if(genderFilter) genderFilter.value = '';
        this.applyFilters();
      });
    }

    // Export and Print functionality
    const exportBtn = document.getElementById('exportBtn');
    const printBtn = document.getElementById('printBtn');

    if(exportBtn){
      exportBtn.addEventListener('click', () => this.exportToCSV());
    }

    if(printBtn){
      printBtn.addEventListener('click', () => window.print());
    }
  },

  applyFilters(){
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const classFilter = document.getElementById('classFilter')?.value || '';
    const deptFilter = document.getElementById('deptFilter')?.value || '';
    const genderFilter = document.getElementById('genderFilter')?.value || '';

    const filtered = this.allStudents.filter(s => {
      // Search filter
      const matchesSearch = !searchTerm || 
        s.full_name.toLowerCase().includes(searchTerm) ||
        s.roll.toLowerCase().includes(searchTerm) ||
        s.email.toLowerCase().includes(searchTerm);

      // Class filter - exact match for specific class divisions
      const matchesClass = !classFilter || s.class_year === classFilter;

      // Department filter
      const matchesDept = !deptFilter || s.department === deptFilter;

      // Gender filter
      const matchesGender = !genderFilter || s.gender === genderFilter;

      return matchesSearch && matchesClass && matchesDept && matchesGender;
    });

    const tbl = document.getElementById('studentsTbody');
    if(tbl) this._renderRows(tbl, filtered);

    // Update count
    const countBadge = document.getElementById('studentCount');
    if(countBadge) countBadge.textContent = filtered.length;
  },

  exportToCSV(){
    const students = JSON.parse(localStorage.getItem('sis_demo_students') || '[]');
    if(students.length === 0){
      utils.showToast('No students to export', 'warning');
      return;
    }

    const rows = [
      ['Roll No', 'Name', 'Class', 'Email', 'Contact', 'Department', 'Semester', 'Gender', 'DOB', 'Address']
    ];

    students.forEach(s => {
      rows.push([
        s.roll,
        s.full_name,
        s.class_year,
        s.email,
        s.contact,
        s.department || '',
        s.semester || '',
        s.gender || '',
        s.dob || '',
        s.address || ''
      ]);
    });

    utils.downloadCSV('students_list.csv', rows);
    utils.showToast('Students exported successfully', 'success');
  },

  loadAndRender(){
    const tbl = document.getElementById('studentsTbody');
    if(!tbl) return;
    tbl.innerHTML = '<tr><td colspan="6" class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></td></tr>';

    // Try fetching from backend API first. If it fails, fallback to localStorage demo data.
    const apiUrl = `${window.API_BASE}/students/`;
    fetch(apiUrl, { credentials: 'same-origin' })
      .then(resp => {
        if(!resp.ok) throw new Error('API not available');
        return resp.json();
      })
      .then(data => {
        // Handle paginated DRF responses or plain arrays
        const list = Array.isArray(data) ? data : (data && data.results ? data.results : []);
        // Map backend student shape to frontend expected fields
        const students = list.map(s => ({
          id: s.id,
          full_name: `${s.first_name || ''} ${s.last_name || ''}`.trim(),
          roll: s.enrollment_number || s.enrollment || '',
          class_year: s.class_year || s.class || '',
          email: s.email || '',
          contact: s.contact || '',
          department: s.department || '',
          semester: s.semester || '',
          gender: s.gender || '',
          dob: s.date_of_birth || s.dob || '',
          address: s.address || ''
        }));
        this.allStudents = students; // Store all students
        this._renderRows(tbl, students);
        
        // Update count
        const countBadge = document.getElementById('studentCount');
        if(countBadge) countBadge.textContent = students.length;
      })
      .catch(() => {
        const students = JSON.parse(localStorage.getItem('sis_demo_students') || '[]');
        this.allStudents = students; // Store all students
        this._renderRows(tbl, students);
        
        // Update count
        const countBadge = document.getElementById('studentCount');
        if(countBadge) countBadge.textContent = students.length;
      });
  },

  _renderRows(tbl, students){
    if(students.length === 0){
      tbl.innerHTML = '<tr><td colspan="6" class="text-center py-4"><i class="bi bi-inbox fs-1 d-block mb-2 text-muted"></i>No students found</td></tr>';
      return;
    }

    students.forEach((s,idx)=>{
      const tr = document.createElement('tr');
      tr.style.animationDelay = `${idx * 0.05}s`;
      tr.innerHTML = `
        <td>${s.roll}</td>
  <td><a class="student-link text-decoration-none" href="/students/${s.id}/" data-id="${s.id}"><strong>${s.full_name}</strong></a></td>
        <td><span class="badge bg-info">${s.class_year}</span></td>
        <td><i class="bi bi-envelope me-1"></i>${s.email}</td>
        <td><i class="bi bi-telephone me-1"></i>${s.contact}</td>
        <td>
            <a class="btn btn-sm btn-outline-primary me-1" href="/students/${s.id}/" title="View Profile">
            <i class="bi bi-eye"></i>
          </a>
            <a class="btn btn-sm btn-outline-secondary me-1 role-edit" href="/students/${s.id}/edit/" title="Edit">
              <i class="bi bi-pencil"></i>
            </a>
          <button class="btn btn-sm btn-outline-danger delete-student role-delete" data-id="${s.id}" data-name="${s.full_name}" title="Delete">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      `;
      tbl.appendChild(tr);
    });

    // Attach delete handlers
    document.querySelectorAll('.delete-student').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = parseInt(e.currentTarget.dataset.id);
        const name = e.currentTarget.dataset.name;
        utils.confirm(`Are you sure you want to delete ${name}?`, () => {
          this.deleteStudent(id);
        });
      });
    });
    // Re-apply role-based UI rules after rendering (safe check)
    if(typeof authModule !== 'undefined' && authModule){
      try{ authModule.applyRoleUI(); }catch(e){ console.warn('applyRoleUI failed', e); }
    }
  },

  deleteStudent(id){
    utils.showLoading();
    const apiUrl = `${window.API_BASE}/students/${id}/`;

    // CSRF helper
    function getCookie(name){
      const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
      return v ? v.pop() : '';
    }

    (async ()=>{
      try{
        const resp = await fetch(apiUrl, {
          method: 'DELETE',
          credentials: 'same-origin',
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });

        if(!resp.ok && resp.status !== 204 && resp.status !== 200){
          throw new Error('API delete failed');
        }

        utils.hideLoading();
        utils.showToast('Student deleted successfully', 'success');
        this.loadAndRender();
      }catch(err){
        // Fallback local deletion
        setTimeout(() => {
          let students = JSON.parse(localStorage.getItem('sis_demo_students') || '[]');
          students = students.filter(s => s.id !== id);
          localStorage.setItem('sis_demo_students', JSON.stringify(students));
          utils.hideLoading();
          utils.showToast('Student deleted locally (API unavailable)', 'warning');
          this.loadAndRender();
        }, 400);
      }
    })();
  },

  filter(q){
    const tbl = document.getElementById('studentsTable');
    if(!tbl) return;
    const rows = tbl.tBodies[0].rows;
    q = q.trim().toLowerCase();
    let visibleCount = 0;

    Array.from(rows).forEach(r=>{
      const isVisible = r.textContent.toLowerCase().includes(q);
      r.style.display = isVisible ? '' : 'none';
      if(isVisible) visibleCount++;
    });

    if(q && visibleCount === 0){
      utils.showToast('No matching students found', 'info');
    }
  }
};

/* Auth / role helper */
const authModule = {
  currentUser: null,
  init(){
    // Returns a Promise that resolves once current user info fetched (or not)
    return fetch(`${window.API_BASE}/me/`, { credentials: 'same-origin' })
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(data => {
        // API returns {is_authenticated, username, groups}
        this.currentUser = data;
        window.currentUser = data;
        this.applyRoleUI();
      })
      .catch(() => {
        // Not authenticated or API not available
        this.currentUser = { is_authenticated: false };
        window.currentUser = this.currentUser;
        this.applyRoleUI();
      });
  },

  isInGroup(name){
    if(!this.currentUser || !this.currentUser.groups) return false;
    return this.currentUser.groups.indexOf(name) !== -1;
  },

  applyRoleUI(){
    // Hide edit/delete by default for anonymous users
    const canEdit = this.isInGroup('Admin') || this.isInGroup('Teacher');
    const canDelete = this.isInGroup('Admin');

    document.querySelectorAll('.role-edit').forEach(el => {
      el.style.display = canEdit ? '' : 'none';
    });
    document.querySelectorAll('.role-delete').forEach(el => {
      el.style.display = canDelete ? '' : 'none';
    });

    // Also update profile edit button if present
    const editBtn = document.getElementById('editProfileBtn');
    if(editBtn){
      if(canEdit){
        // keep display as set by profileModule
      } else {
        editBtn.style.display = 'none';
      }
    }
  }
};

/* Add student form handling */
const addStudentModule = {
  init(){
    const form = document.getElementById('addStudentForm');
    if(!form) return;
    
    // Add real-time validation
    form.querySelectorAll('input[required], select[required]').forEach(field => {
      field.addEventListener('blur', () => this.validateField(field));
      field.addEventListener('input', () => {
        if(field.classList.contains('is-invalid')){
          this.validateField(field);
        }
      });
    });
    
    form.addEventListener('submit', (e)=>{
      e.preventDefault();

      // Validate all fields
      let isValid = true;
      form.querySelectorAll('input[required], select[required]').forEach(field => {
        if(!this.validateField(field)){
          isValid = false;
        }
      });

      if(!isValid){
        utils.showToast('Please fill all required fields correctly', 'error');
        return;
      }

      utils.showLoading();

      const fd = new FormData(form);
      const fullName = (fd.get('full_name') || '').trim();
      const [firstName, ...rest] = fullName.split(' ');
      const lastName = rest.join(' ');

      const payload = {
        first_name: firstName || '',
        last_name: lastName || '',
        enrollment_number: fd.get('roll_number') || '',
        class_year: fd.get('class_year') || '',
        department: fd.get('department') || '',
        semester: fd.get('semester') ? parseInt(fd.get('semester')) : null,
        gender: fd.get('gender') || '',
        date_of_birth: fd.get('dob') || null,
        email: fd.get('email') || '',
        contact: fd.get('contact') || '',
        address: fd.get('address') || ''
      };

      // CSRF helper (reads csrftoken cookie)
      function getCookie(name){
        const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return v ? v.pop() : '';
      }

      const apiUrl = `${window.API_BASE}/students/`;

      (async ()=>{
        try{
          const resp = await fetch(apiUrl, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
          });

          if(!resp.ok){
            throw new Error('API error');
          }

          utils.hideLoading();
          utils.showToast('Student registered successfully!', 'success');
    setTimeout(() => { window.location.href = '/students/'; }, 800);
        }catch(err){
          // Fallback to localStorage if API fails
          const student = {
            id: Date.now(),
            full_name: fd.get('full_name'),
            roll: fd.get('roll_number'),
            class_year: fd.get('class_year'),
            department: fd.get('department'),
            semester: fd.get('semester'),
            gender: fd.get('gender'),
            dob: fd.get('dob'),
            email: fd.get('email'),
            contact: fd.get('contact'),
            address: fd.get('address')
          };
          const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
          students.push(student);
          localStorage.setItem('sis_demo_students', JSON.stringify(students));

          utils.hideLoading();
          utils.showToast('Student registered locally (API unavailable)', 'warning');
          setTimeout(() => { window.location.href = '/students/'; }, 600);
        }
      })();
    });
  },
  
  validateField(field){
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    if(field.hasAttribute('required') && !value){
      isValid = false;
      message = 'This field is required';
    } else if(field.type === 'email' && value && !this.isValidEmail(value)){
      isValid = false;
      message = 'Please enter a valid email';
    } else if(field.type === 'tel' && value && !this.isValidPhone(value)){
      isValid = false;
      message = 'Please enter a valid phone number';
    }
    
    if(isValid){
      field.classList.remove('is-invalid');
      field.classList.add('is-valid');
    } else {
      field.classList.remove('is-valid');
      field.classList.add('is-invalid');
      const feedback = field.nextElementSibling;
      if(feedback && feedback.classList.contains('invalid-feedback')){
        feedback.textContent = message;
      }
    }
    
    return isValid;
  },
  
  isValidEmail(email){
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  },
  
  isValidPhone(phone){
    return /^[\d\s\+\-\(\)]{10,}$/.test(phone);
  }
};

/* Edit student form handling */
const editStudentModule = {
  init(){
    // Attempt to read id from query string first, then from pathname (/students/<id>/edit/)
    const params = new URLSearchParams(location.search);
    let id = params.get('id');
    if(!id){
      // e.g. /students/123/edit/ or /students/123/
      const parts = location.pathname.replace(/\/+$/, '').split('/');
      // find the last numeric-ish segment
      for(let i = parts.length - 1; i >= 0; i--){
        if(parts[i] && /\d+/.test(parts[i])){ id = parts[i]; break; }
      }
    }
    if(!id) return;

    const form = document.getElementById('editStudentForm');
    if(!form) return;

    // Prefill from API or localStorage
    const apiUrl = `${window.API_BASE}/students/${id}/`;
    fetch(apiUrl, { credentials: 'same-origin' })
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(s => this.populateFormFromApi(s))
      .catch(() => this.populateFormFromLocal(id));

    // validation handlers
    form.querySelectorAll('input[required], select[required]').forEach(field => {
      field.addEventListener('blur', () => addStudentModule.validateField(field));
      field.addEventListener('input', () => {
        if(field.classList.contains('is-invalid')) addStudentModule.validateField(field);
      });
    });

    form.addEventListener('submit', (e)=>{
      e.preventDefault();

      let isValid = true;
      form.querySelectorAll('input[required], select[required]').forEach(field => {
        if(!addStudentModule.validateField(field)) isValid = false;
      });
      if(!isValid){ utils.showToast('Please fill all required fields correctly', 'error'); return; }

      utils.showLoading();
      const fd = new FormData(form);
      const fullName = (fd.get('full_name') || '').trim();
      const [firstName, ...rest] = fullName.split(' ');
      const lastName = rest.join(' ');

      const payload = {
        first_name: firstName || '',
        last_name: lastName || '',
        enrollment_number: fd.get('roll_number') || '',
        class_year: fd.get('class_year') || '',
        department: fd.get('department') || '',
        semester: fd.get('semester') ? parseInt(fd.get('semester')) : null,
        gender: fd.get('gender') || '',
        date_of_birth: fd.get('dob') || null,
        email: fd.get('email') || '',
        contact: fd.get('contact') || '',
        address: fd.get('address') || ''
      };

      function getCookie(name){ const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)'); return v ? v.pop() : ''; }

      (async ()=>{
        try{
          const resp = await fetch(apiUrl, {
            method: 'PATCH',
            credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify(payload)
          });

          if(!resp.ok) throw new Error('API update failed');

          utils.hideLoading(); utils.showToast('Student updated successfully', 'success');
          setTimeout(()=> { window.location.href = '/students/'; }, 700);
        }catch(err){
          // fallback: update localStorage
          setTimeout(()=>{
            let students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
            students = students.map(s => {
              if(String(s.id) === String(id)){
                return Object.assign({}, s, {
                  full_name: fd.get('full_name'),
                  roll: fd.get('roll_number'),
                  class_year: fd.get('class_year'),
                  department: fd.get('department'),
                  semester: fd.get('semester'),
                  gender: fd.get('gender'),
                  dob: fd.get('dob'),
                  email: fd.get('email'),
                  contact: fd.get('contact'),
                  address: fd.get('address')
                });
              }
              return s;
            });
            localStorage.setItem('sis_demo_students', JSON.stringify(students));
            utils.hideLoading(); utils.showToast('Student updated locally (API unavailable)', 'warning');
            setTimeout(()=> { window.location.href = '/students/'; }, 700);
          }, 400);
        }
      })();
    });
  },

  populateFormFromApi(s){
    const full = `${s.first_name} ${s.last_name}`.trim();
    document.getElementById('editStudentId').value = s.id;
    document.getElementById('full_name').value = full;
    document.getElementById('roll_number').value = s.enrollment_number || '';
    document.getElementById('class_year').value = s.class_year || '';
    document.getElementById('department').value = s.department || '';
    document.getElementById('semester').value = s.semester || '';
    document.getElementById('gender').value = s.gender || '';
    document.getElementById('dob').value = s.date_of_birth || '';
    document.getElementById('email').value = s.email || '';
    document.getElementById('contact').value = s.contact || '';
    document.getElementById('address').value = s.address || '';
  },

  populateFormFromLocal(id){
    const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
    const s = students.find(x=>String(x.id)===String(id));
    if(!s) return;
    document.getElementById('editStudentId').value = s.id;
    document.getElementById('full_name').value = s.full_name || '';
    document.getElementById('roll_number').value = s.roll || '';
    document.getElementById('class_year').value = s.class_year || '';
    document.getElementById('department').value = s.department || '';
    document.getElementById('semester').value = s.semester || '';
    document.getElementById('gender').value = s.gender || '';
    document.getElementById('dob').value = s.dob || '';
    document.getElementById('email').value = s.email || '';
    document.getElementById('contact').value = s.contact || '';
    document.getElementById('address').value = s.address || '';
  }
};

/* Profile module */
const profileModule = {
  init(){
    // Profile page may use ?roll=... or be served at /students/<id>/
    const params = new URLSearchParams(location.search);
    let roll = params.get('roll');
    if(!roll){
      // try to extract id from pathname and use that as identifier
      const parts = location.pathname.replace(/\/+$/, '').split('/');
      for(let i = parts.length - 1; i >= 0; i--){
        if(parts[i] && /\d+/.test(parts[i])){ roll = parts[i]; break; }
      }
    }
    if(!roll) return;
    
    // Try to fetch student from API (handle paginated responses)
    const apiUrl = `${window.API_BASE}/students/`;
    fetch(apiUrl, { credentials: 'same-origin' })
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(data => {
        const list = Array.isArray(data) ? data : (data && data.results ? data.results : []);
        const student = list.find(s => String(s.enrollment_number) === String(roll) || String(s.enrollment) === String(roll) || String(s.id) === String(roll));
        if(student) {
          this.displayStudent(student);
        } else {
          this.loadFromLocalStorage(roll);
        }
      })
      .catch(() => {
        this.loadFromLocalStorage(roll);
      });
  },
  
  loadFromLocalStorage(roll){
    const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
    const s = students.find(x=>x.roll===roll) || students[0];
    if(!s) return;
    // local storage student shape differs; pass through and let displayStudent handle it
    this.displayStudent(s);
  },
  
  displayStudent(s){
    // Handle both API student shape and localStorage demo shape
    const id = s.id || s.id;
    const first = s.first_name || (s.full_name ? s.full_name.split(' ')[0] : '');
    const last = s.last_name || (s.full_name ? s.full_name.split(' ').slice(1).join(' ') : '');
    const fullName = `${first} ${last}`.trim() || (s.full_name || '');
    const roll = s.enrollment_number || s.roll || '';
    const email = s.email || '';
    const contact = s.contact || '';
    const class_year = s.class_year || s.classYear || s.class_year || s.class || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.class_year || s.classYear || s.class_year;
    const department = s.department || '';
    const semester = s.semester || '';
    const gender = s.gender || '';
    const dob = s.date_of_birth || s.dob || '';
    const address = s.address || '';

    if(document.getElementById('studentName')) {
      document.getElementById('studentName').textContent = fullName || '--';
    }
    if(document.getElementById('studentRoll')) {
      document.getElementById('studentRoll').textContent = 'Roll: ' + (roll || '--');
    }
    if(document.getElementById('profileName')) {
      document.getElementById('profileName').textContent = fullName || 'Student Profile';
    }
    if(document.getElementById('profileRoll')) {
      document.getElementById('profileRoll').textContent = 'Roll: ' + (roll || '--');
    }
    // Details
    if(document.getElementById('profileEmail')) document.getElementById('profileEmail').textContent = email || 'N/A';
    if(document.getElementById('profileContact')) document.getElementById('profileContact').textContent = contact || 'N/A';
    if(document.getElementById('profileClass')) document.getElementById('profileClass').textContent = class_year || 'N/A';
    if(document.getElementById('profileDepartment')) document.getElementById('profileDepartment').textContent = department || 'N/A';
    if(document.getElementById('profileSemester')) document.getElementById('profileSemester').textContent = semester || 'N/A';
    if(document.getElementById('profileGender')) document.getElementById('profileGender').textContent = gender || 'N/A';
    if(document.getElementById('profileDOB')) document.getElementById('profileDOB').textContent = dob || 'N/A';
    if(document.getElementById('profileAddress')) document.getElementById('profileAddress').textContent = address || 'N/A';

    // Show edit button if present
    const editBtn = document.getElementById('editProfileBtn');
    if(editBtn){
      if(id){
        editBtn.href = `/students/${id}/edit/`;
        editBtn.style.display = '';
      } else {
        // If no id (unlikely for API), try to find by roll from localStorage
        const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
        const found = students.find(x => x.roll === roll);
        if(found && found.id){ editBtn.href = `/students/${found.id}/edit/`; editBtn.style.display = ''; }
      }
    }
  }
};

/* Attendance module */
const attendanceModule = {
  init(){
    const select = document.getElementById('selectClass');
    const tbody = document.getElementById('attendanceTbody');
    const dateInput = document.getElementById('attDate');
    if(!select || !tbody) return;
    
    // Set today's date
    if(dateInput) dateInput.value = utils.formatDate(new Date());
    
    const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
    // populate class select with unique classes
    const classes = [...new Set(students.map(s=>s.class_year))];
    select.innerHTML = '<option value="">-- Select Class --</option>' + classes.map(c=>`<option value="${c}">${c}</option>`).join('');
    
    // render rows
    function renderRows(){
      const cls = select.value;
      if(!cls){
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-4">Please select a class</td></tr>';
        return;
      }
      
      const filtered = students.filter(s=>s.class_year===cls);
      tbody.innerHTML = '';
      
      filtered.forEach((s,i)=>{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${i+1}</td>
          <td>${s.roll}</td>
          <td>${s.full_name}</td>
          <td class="text-center">
            <input type="checkbox" class="form-check-input attendance-check" data-roll="${s.roll}" checked>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
    
    select.addEventListener('change', renderRows);
    renderRows();
    
    // Select all / Deselect all functionality
    const form = document.getElementById('attendanceForm');
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'btn btn-outline-secondary me-2';
    toggleBtn.innerHTML = '<i class="bi bi-check-all me-1"></i> Toggle All';
    toggleBtn.addEventListener('click', () => {
      const checkboxes = document.querySelectorAll('.attendance-check');
      const allChecked = Array.from(checkboxes).every(cb => cb.checked);
      checkboxes.forEach(cb => cb.checked = !allChecked);
    });
    
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.parentElement.insertBefore(toggleBtn, submitBtn);
    
    form.addEventListener('submit', function(e){
      e.preventDefault();
      const date = dateInput.value || utils.formatDate(new Date());
      const cls = select.value;
      
      if(!cls){
        utils.showToast('Please select a class', 'warning');
        return;
      }
      
      const checked = Array.from(document.querySelectorAll('.attendance-check'))
        .filter(c=>c.checked)
        .map(c=>c.dataset.roll);
      
      utils.showLoading();
      
      setTimeout(() => {
        const attendance = JSON.parse(localStorage.getItem('sis_demo_attendance')||'{}');
        attendance[`${date}_${cls}`] = checked;
        localStorage.setItem('sis_demo_attendance', JSON.stringify(attendance));
        
        utils.hideLoading();
        utils.showToast(`Attendance saved for ${cls} (${checked.length} present)`, 'success');
      }, 500);
    });
  }
};

/* Marks module */
const marksModule = {
  init(){
    const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
    const selectClass = document.getElementById('marksClass');
    const selectSubject = document.getElementById('marksSubject');
    const tbody = document.getElementById('marksTbody');
    const examInput = document.getElementById('examName');
    
    if(!selectClass || !tbody) return;
    
    const classes = [...new Set(students.map(s=>s.class_year))];
    selectClass.innerHTML = '<option value="">-- Select Class --</option>' + classes.map(c=>`<option value="${c}">${c}</option>`).join('');
    selectSubject.innerHTML = ['Data Structures','DBMS','OS','Web Development','Machine Learning'].map(s=>`<option>${s}</option>`).join('');
    
    function render(){
      const cls = selectClass.value;
      if(!cls){
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">Please select a class</td></tr>';
        return;
      }
      
      const list = students.filter(s=>s.class_year===cls);
      tbody.innerHTML = '';
      
      list.forEach((s,i)=>{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${i+1}</td>
          <td>${s.roll}</td>
          <td>${s.full_name}</td>
          <td><input class="form-control mark-input" type="number" min="0" max="100" value="0" placeholder="Marks"></td>
          <td><input class="form-control total-input" type="number" min="1" max="100" value="100" placeholder="Total"></td>
        `;
        tbody.appendChild(tr);
      });
    }
    
    selectClass.addEventListener('change', render);
    render();
    
    document.getElementById('marksForm').addEventListener('submit', function(e){
      e.preventDefault();
      
      const cls = selectClass.value;
      const subject = selectSubject.value;
      const exam = examInput.value.trim() || 'Exam';
      
      if(!cls){
        utils.showToast('Please select a class', 'warning');
        return;
      }
      
      utils.showLoading();
      
      setTimeout(() => {
        const marksData = [];
        document.querySelectorAll('#marksTbody tr').forEach(tr => {
          const roll = tr.children[1].textContent;
          const marks = tr.querySelector('.mark-input').value;
          const total = tr.querySelector('.total-input').value;
          marksData.push({roll, marks, total});
        });
        
        const marksStore = JSON.parse(localStorage.getItem('sis_demo_marks')||'{}');
        marksStore[`${cls}_${subject}_${exam}`] = marksData;
        localStorage.setItem('sis_demo_marks', JSON.stringify(marksStore));
        
        utils.hideLoading();
        utils.showToast(`Marks saved for ${subject} - ${exam}`, 'success');
      }, 500);
    });
  }
};

/* Init on DOM ready */
document.addEventListener('DOMContentLoaded', function(){
  sidebarController.init();
  demo.seed();
  // Initialize auth first so role-based UI can be applied when rendering lists
  authModule.init().finally(() => {
    studentsModule.init();
    addStudentModule.init();
    editStudentModule.init();
    profileModule.init();
    attendanceModule.init();
    marksModule.init();
  });
  
  // populate dashboard stats from API
  if(document.getElementById('statStudents')){
    fetch(`${window.API_BASE}/students/`, { credentials: 'same-origin' })
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(data => {
        document.getElementById('statStudents').textContent = data.length;
      })
      .catch(() => {
        const students = JSON.parse(localStorage.getItem('sis_demo_students')||'[]');
        document.getElementById('statStudents').textContent = students.length;
      });
  }
  
  if(document.getElementById('statAttendance')){
    fetch(`${window.API_BASE}/attendance/`, { credentials: 'same-origin' })
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(data => {
        document.getElementById('statAttendance').textContent = data.length;
      })
      .catch(() => {
        const attendance = JSON.parse(localStorage.getItem('sis_demo_attendance')||'{}');
        document.getElementById('statAttendance').textContent = Object.keys(attendance).length;
      });
  }
  
  if(document.getElementById('statSubjects')){
    document.getElementById('statSubjects').textContent = '5';
  }
  
  if(document.getElementById('statMarks')){
    fetch(`${window.API_BASE}/marks/`, { credentials: 'same-origin' })
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(data => {
        document.getElementById('statMarks').textContent = data.length;
      })
      .catch(() => {
        const marks = JSON.parse(localStorage.getItem('sis_demo_marks')||'{}');
        document.getElementById('statMarks').textContent = Object.keys(marks).length;
      });
  }
  
  // Add interactivity to stat cards
  document.querySelectorAll('.stat-card').forEach((card, idx) => {
    card.style.animationDelay = `${idx * 0.1}s`;
  });
});

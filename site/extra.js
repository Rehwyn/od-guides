// Small accessibility adapter for the theme's checkbox-backed menu labels.
document.addEventListener('DOMContentLoaded', () => {
  const controls = [
    ['.md-header label[for="__drawer"]', '__drawer', 'Guide library'],
    ['.md-sidebar-button[for="__toc"]', '__toc', 'On this page'],
  ];
  for (const [selector, id, name] of controls) {
    const label = document.querySelector(selector);
    const input = document.getElementById(id);
    if (!label || !input) continue;
    label.tabIndex = 0;
    label.setAttribute('role', 'button');
    label.setAttribute('aria-label', name);
    const sync = () => label.setAttribute('aria-expanded', String(input.checked));
    sync();
    input.addEventListener('change', sync);
    label.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        event.stopImmediatePropagation();
        input.checked = !input.checked;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
    label.addEventListener('keyup', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        event.stopImmediatePropagation();
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && input.checked) {
        input.checked = false;
        input.dispatchEvent(new Event('change', { bubbles: true }));
        label.focus();
      }
    });
    document.querySelectorAll('.md-nav a').forEach(link => {
      link.addEventListener('click', () => {
        if (input.checked) {
          input.checked = false;
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      });
    });
  }
});

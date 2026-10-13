const citations = {
  zeroov: `@misc{li2026trainingfree,
  title={Training-Free Open-Vocabulary Visual Grounding for Remote Sensing Images and Videos},
  author={Ke Li and Di Wang and Yongshan Zhu and Ting Wang and Weiping Ni and Tao Lei and Quan Wang and Xinbo Gao},
  year={2026},
  eprint={2606.16124},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2606.16124}
}`,
  provg: `@misc{li2026provg,
  title={ProVG: Progressive Visual Grounding via Language Decoupling for Remote Sensing Imagery},
  author={Ke Li and Ting Wang and Di Wang and Yongshan Zhu and Yiming Zhang and Tao Lei and Quan Wang},
  year={2026},
  eprint={2604.01893},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2604.01893}
}`,
  ddtm: `@misc{gao2025dualbranch,
  title={A Dual-Branch Local-Global Framework for Cross-Resolution Land Cover Mapping},
  author={Peng Gao and Ke Li and Di Wang and Yongshan Zhu and Yiming Zhang and Xuemei Luo and Yifeng Wang},
  year={2025},
  eprint={2512.19990},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2512.19990}
}`
};
const dialog = document.querySelector('#citation-dialog');
const text = document.querySelector('#citation-text');
const status = document.querySelector('#copy-status');
document.querySelector('#year').textContent = new Date().getFullYear();
document.querySelectorAll('.bibtex-button').forEach(button => {
  button.addEventListener('click', () => {
    text.textContent = citations[button.dataset.paper];
    status.textContent = '';
    dialog.showModal();
  });
});
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const rect = dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
});
document.querySelector('#copy-citation').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(text.textContent);
    status.textContent = 'Citation copied.';
  } catch {
    const range = document.createRange();
    range.selectNodeContents(text);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = 'Citation selected. Press Ctrl+C or ⌘C to copy.';
  }
});

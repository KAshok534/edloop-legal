'use strict';
// Real questions from NTA's official JEE Main papers, answers from the official final key
// (IIT-APP content: q-2026-04-02-m-p08, q-2026-04-05-m-c01, q-2026-04-04-m-m04).
const examples = [
  { subject: 'Physics', topic: 'Thermodynamics · JEE Main 2026, 2 Apr Shift 1', question: 'Heat is supplied to a diatomic gas at constant pressure. Then the ratio of ΔQ : ΔU : ΔW is ________.', answers: ['2 : 3 : 5', '5 : 3 : 2', '2 : 5 : 7', '7 : 5 : 2'], correct: 3, keyIdea: 'At constant pressure ΔQ : ΔU : ΔW = Cp : Cv : R. For a diatomic gas Cv = 5R/2 and Cp = 7R/2, so the ratio is 7 : 5 : 2.', mistake: 'Using monatomic values (Cv = 3R/2), which gives 5 : 3 : 2.' },
  { subject: 'Chemistry', topic: 'Mole Concept · JEE Main 2026, 5 Apr Shift 1', question: 'How many grams of residue is obtained by heating 2.76 g of silver carbonate? (Given: molar mass of C, O and Ag are 12, 16 and 108 g mol⁻¹ respectively)', answers: ['1.08 g', '2.16 g', '3.24 g', '4.32 g'], correct: 1, keyIdea: 'Ag₂CO₃ → 2Ag + CO₂ + ½O₂, and the residue is silver metal. 2.76 g is 0.01 mol (M = 276), giving 0.02 mol Ag = 2.16 g.', mistake: 'Stopping at Ag₂O, which gives 2.32 g.' },
  { subject: 'Maths', topic: 'Sets, Relations & Functions · JEE Main 2026, 4 Apr Shift 1', question: 'The number of functions f : {1, 2, 3, 4} → {a, b, c}, which are not onto, is:', answers: ['48', '45', '51', '35'], correct: 1, keyIdea: 'All functions: 3⁴ = 81. Onto functions: 3⁴ − 3·2⁴ + 3 = 36. Not onto: 81 − 36 = 45.', mistake: 'Subtracting 3·2⁴ without adding back the 3 constant functions.' }
];
let currentExample = 0;
const feedback = document.querySelector('#answer-feedback');
const solution = document.querySelector('#solution');
const solutionButton = document.querySelector('#show-solution');
const radios = [...document.querySelectorAll('input[name="answer"]')];
function resetFeedback() { feedback.textContent = ''; feedback.className = 'answer-feedback'; }
document.querySelectorAll('[data-topic]').forEach(button => button.addEventListener('click', () => {
  currentExample = Number(button.dataset.topic);
  const example = examples[currentExample];
  document.querySelectorAll('[data-topic]').forEach(topic => { const active = topic === button; topic.classList.toggle('active', active); topic.setAttribute('aria-pressed', String(active)); });
  document.querySelector('#demo-subject').textContent = example.subject;
  document.querySelector('#question-topic').textContent = example.topic;
  document.querySelector('#question-text').textContent = example.question;
  document.querySelectorAll('[data-answer]').forEach((answer, index) => { answer.textContent = example.answers[index]; });
  radios.forEach(radio => { radio.checked = false; });
  solution.querySelector('[data-key]').textContent = example.keyIdea;
  solution.querySelector('[data-mistake]').textContent = example.mistake;
  solution.hidden = true;
  solutionButton.setAttribute('aria-expanded', 'false');
  solutionButton.innerHTML = 'View solution <span aria-hidden="true">⌄</span>';
  resetFeedback();
}));
radios.forEach(radio => radio.addEventListener('change', resetFeedback));
document.querySelector('#check-answer').addEventListener('click', () => {
  const selected = radios.find(radio => radio.checked);
  if (!selected) { feedback.textContent = 'Choose an answer first.'; radios[0].focus(); return; }
  const correct = Number(selected.value) === examples[currentExample].correct;
  feedback.className = `answer-feedback ${correct ? 'correct' : 'incorrect'}`;
  feedback.textContent = correct ? 'That’s right: +4 in the exam. View the solution to check your reasoning.' : 'Not quite: −1 in the exam. Try again, or open the solution.';
});
solutionButton.addEventListener('click', () => {
  solution.hidden = !solution.hidden;
  solutionButton.setAttribute('aria-expanded', String(!solution.hidden));
  solutionButton.innerHTML = `${solution.hidden ? 'View' : 'Hide'} solution <span aria-hidden="true">${solution.hidden ? '⌄' : '⌃'}</span>`;
});

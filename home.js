'use strict';
const examples = [
  { topic: 'Kinematics · Uniform acceleration', question: 'Starting from rest, a particle accelerates uniformly. It covers 7 m during the fourth second. How far does it travel during the third second?', answers: ['3 m', '5 m', '7 m', '9 m'], correct: 1, heading: 'Distance in the nth second', explanation: 'For a start from rest, sₙ = a(n − ½). So 7 = a × 3.5, giving a = 2 m/s². During the third second: 2 × 2.5 = 5 m.' },
  { topic: 'Laws of Motion · Newton’s second law', question: 'A net force acts on a 2 kg block and gives it an acceleration of 3 m/s². What is the magnitude of the net force?', answers: ['1.5 N', '5 N', '6 N', '9 N'], correct: 2, heading: 'Apply Newton’s second law', explanation: 'Net force equals mass times acceleration: F = ma. Here, F = 2 × 3 = 6 N. Use the net force, which includes all the forces acting on the block.' },
  { topic: 'Current Electricity · Ohm’s law', question: 'A current of 2 A flows through a resistor of resistance 10 Ω. What is the potential difference across the resistor?', answers: ['5 V', '10 V', '12 V', '20 V'], correct: 3, heading: 'Relate voltage, current and resistance', explanation: 'Ohm’s law gives V = IR. With I = 2 A and R = 10 Ω, the potential difference is 2 × 10 = 20 V.' }
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
  document.querySelector('#question-topic').textContent = example.topic;
  document.querySelector('#question-text').textContent = example.question;
  document.querySelectorAll('[data-answer]').forEach((answer, index) => { answer.textContent = example.answers[index]; });
  radios.forEach(radio => { radio.checked = false; });
  solution.querySelector('strong').textContent = example.heading;
  solution.querySelector('p').textContent = example.explanation;
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
  feedback.textContent = correct ? 'That’s right. View the solution to check your reasoning.' : 'Not quite. Try again, or open the solution to see the steps.';
});
solutionButton.addEventListener('click', () => {
  solution.hidden = !solution.hidden;
  solutionButton.setAttribute('aria-expanded', String(!solution.hidden));
  solutionButton.innerHTML = `${solution.hidden ? 'View' : 'Hide'} solution <span aria-hidden="true">${solution.hidden ? '⌄' : '⌃'}</span>`;
});

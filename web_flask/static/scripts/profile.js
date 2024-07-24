// Handles profile page

$(function () { 

    // Populate User's Questions Section
    const userId = $(".id").text().split(" ")[1];
    const questionsContainer = $(".questions .content");
    const answersContainer = $(".answers .content");
    let questionIndex = 0;
    let answerIndex = 0;
    $.ajax({
          url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${userId}/questions/${questionIndex}`,
          type: 'GET',
          success: function (questions) {
                      if (questions.length > 0) {
                                questionIndex += 5;
                                for (const q of questions) {
                                    questionsContainer.append(`
                                                  <div class="question">
                                                    <h3><a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${q.id}">${q.title}</a></h3>
                                                    <p>Asked at: <span id="${q.id}-created_at">${q.created_at.replace("T", " ") + " UTC"}</span>, Updated at: <span id="${q.id}-updated_at">${q.updated_at.replace("T", " ") + " UTC"}</span></p>
                                                  </div>
                                    `)
                                }
                                $(".questions").append('<p class="more" id="more-questions">More ...</p>')
                                const moreQuestions = $("#more-questions");
                                moreQuestions.on('click', function () {
                                  $.ajax({
                                    url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${userId}/questions/${questionIndex}`,
                                    type: 'GET',
                                    success: function (questions) {
                                                if (questions.length > 0) {
                                                  questionIndex += 5;
                                                  for (const q of questions) {
                                                    questionsContainer.append(`
                                                                  <div class="question">
                                                                    <h3><a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${q.id}">${q.title}</a></h3>
                                                                    <p>Asked at: <span id="${q.id}-created_at">${q.created_at.replace("T", " ") + " UTC"}</span>, Updated at: <span id="${q.id}-updated_at">${q.updated_at.replace("T", " ") + " UTC"}</span></p>
                                                                  </div>
                                                    `)
                                                  }
                                                } else {
                                                  alert("No more questions")
                                                }
                                  }
            })
          })
          // Populate User's Answers Section

                $.ajax({
                  url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${userId}/answers/${answerIndex}`,
                  type: 'GET',
                  success: function (answers) {
                    answerIndex += 5;
                    if (answers.length > 0) {
                      for (const a of answers) {
                        answersContainer.append(`
                            <div class="answer" id="${a.id}">
                              <p>For: <a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${a.question_id}" class="${a.question_id}-question-link"></a></p>
                              <p>Aswered at: <span id=${a.id}-created_at>${a.created_at.replace("T", " ") + " UTC"}</span>, Updated at: <span id=${a.id}-updated_at>${a.updated_at.replace("T", " ") + " UTC"}</span></p>
                            </div>
                        `)
                        $.ajax({
                          url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${a.question_id}`,
                          type: 'GET',
                          success: function (question) {
                            const questionTitle = $(`.${a.question_id}-question-link`);
                            questionTitle.text(question.title)
                          }
                        })
                      }
                      $(".container .answers").append('<p class="more" id="more-answers">More ...</p>');
                      const moreAnswers = $("#more-answers");
                      moreAnswers.on("click", function () {
                        console.log("More answers");
                        $.ajax({
                          url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${userId}/answers/${answerIndex}`,
                          type: 'GET',
                          success: function (answers) {
                            answerIndex += 5;
                            if (answers.length > 0) {
                              console.log(answers.length)
                              for (const a of answers) {
                                answersContainer.append(`
                                    <div class="answer">
                                      <p>For: <a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${a.question_id}" class="${a.question_id}-question-link"></a></p>
                                      <p>Aswered at: <span>${a.created_at.replace("T", " ") + " UTC"}</span>, Updated at: <span>${a.updated_at.replace("T", " ") + " UTC"}</span></p>
                                    </div>
                                `)
                                $.ajax({
                                  url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${a.question_id}`,
                                  type: 'GET',
                                  success: function (question) {
                                    const questionTitle = $(`.${a.question_id}-question-link`);
                                    questionTitle.text(question.title)
                                  }
                                })
                              }
                            } else {
                              alert('No more answers')
                            }
                          }
                        })
                      })
                    } else {
                        answersContainer.text("No answrs")
                    }
                  }
                })
              } else {
            questionsContainer.text("No questions")

            // Populate User's Answers Section

            $.ajax({
              url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${userId}/answers/${answerIndex}`,
              type: 'GET',
              success: function (answers) {
                answerIndex += 5;
                if (answers.length > 0) {
                  for (const a of answers) {
                    answersContainer.append(`
                        <div class="answer">
                        <p>For: <a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${a.question_id}" class="${a.question_id}-question-link"></a></p>
                        <p>Aswered at: <span>${a.created_at.replace("T", " ") + " UTC"}</span>, Updated at: <span>${a.updated_at.replace("T", " ") + " UTC"}</span></p>
                        </div>
                    `)
                    $.ajax({
                      url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${a.question_id}`,
                      type: 'GET',
                      success: function (question) {
                        const questionTitle = $(`.${a.question_id}-question-link`);
                        questionTitle.text(question.title)
                      }
                    })
                  }  
                  $(".container .answers").append('<p class="more" id="more-answers">More ...</p>');
                  const moreAnswers = $("#more-answers");
                  moreAnswers.on("click", function () {
                  console.log("More answers");
                    $.ajax({
                      url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${userId}/answers/${answerIndex}`,
                      type: 'GET',
                      success: function (answers) {
                        answerIndex += 5;
                        if (answers.length > 0) {
                          for (const a of answers) {
                            answersContainer.append(`
                                <div class="answer">
                                <p>For: <a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${a.question_id}" class="${a.question_id}-question-link"></a></p>
                                <p>Aswered at: <span>${a.created_at.replace("T", " ") + " UTC"}</span>, Updated at: <span>${a.updated_at.replace("T", " ") + " UTC"}</span></p>
                                </div>
                            `)
                            $.ajax({
                              url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${a.question_id}`,
                              type: 'GET',
                              success: function (question) {
                                const questionTitle = $(`.${a.question_id}-question-link`);
                                questionTitle.text(question.title)
                              }
                            })
                          }
                        } else {
                          alert('No more answers')
                        }
                      }
                    })
                  })

                } else {
                    answersContainer.text("No answers");
                }
              }
            })
        }
      }
    })
});

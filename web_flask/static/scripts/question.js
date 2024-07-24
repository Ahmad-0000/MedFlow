// Handles question page

$(function () {
    const questionInfoContainer = $(".question-info");
    const questionId = $(".question").attr("data-id");

    // Get the question
    $.ajax({
        url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${questionId}`,
        type: "GET",
        success: function (q) {
            questionInfoContainer.append(`
                <h3 class="title">${q.title}</h3>
                <p class="metadata">By <a href="/medflow/users/${q.user_id}" id="question-user-link"></a> - At <span class="created_at">${q.created_at.replace("T", " ") + " UTC"}</span> - Updtaed at <span class="updated_at">${q.updated_at.replace("T"," ") + " UTC"}</span></p>
                <p class="body">${q.body}</p>
            `)
            const userLink = $("#question-user-link");
            $.ajax({
                url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${q.user_id}`,
                type: "GET",
                success: function (user) {
                    userLink.text(user.first_name + " " + user.last_name);
                }
            });
            // Get the question comments
            $.ajax({
                url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${questionId}/comments`,
                type: 'GET',
                success: function (qComs) {
                    const qCommetnsContainer = $(".question .comments");
                    if (qComs.length > 0) { // There is comments
                        for (const qCom of qComs) {
                            qCommetnsContainer.append(`
                                <div class="com">
                                    <ul class="options">
                                        <li><a href="http://web-01.ahmad-basheer.tech:5000/medflow/questions/${qCom.question_id}/update_comment/${qCom.id}">Edit</a></li>
                                        <li><form action="http://web-01.ahmad-basheer.tech:5000/medflow/del_qcomment/${qCom.id}", method="post"><input type="submit" value="Delete" class="del"></form></li>
                                    </ul>
                                    <p class="metadata">Comment by <a href="http://web-01.ahmad-basheer.tech:5000/medflow/users/${qCom.user_id}" class="${qCom.user_id}-question-comment-user-link"></a> - At <span">${qCom.created_at.replace("T", " ") + " UTC"}</span> - Updtaed at <span>${qCom.updated_at.replace("T", " ") + " UTC"}</span></p>
                                    <p class="body">${qCom.body}</p>
                                    <div class="comment-stats">
                                    </div>
                                </div>
                            `);
                            // Get the comment user
                            $.ajax({
                                url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${qCom.user_id}`,
                                type: 'GET',
                                success: function (user) {
                                    const userLink = $(`.${user.id}-question-comment-user-link`);
                                    userLink.text(user.first_name + " " + user.last_name);
                                }
                            })
                        }
                    } else { 
                        qCommetnsContainer.text("No Comments");
                        qCommetnsContainer.addClass("center-text");
                    }
                }
            });
        }
    });

    // Get the answers
    const answersContainer = $(".answers");
    $.ajax({
        url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${questionId}/answers`,
        type: 'GET',
        success: function (answers) {
            if (answers.length > 0) {
                for (const a of answers) {
                    answersContainer.append(`
                        <div class="answer">
                            <ul class="options">
                                <li><a href="http://web-01.ahmad-basheer.tech:5000/medflow/update_answer/${a.id}">Edit</a></li>
                                <li><a href="http://web-01.ahmad-basheer.tech:5000/medflow/add_answer_comment/${a.id}">Comment</a></li>
                                <li><form action="http://web-01.ahmad-basheer.tech:5000/medflow/del_answer/${a.id}", method="post"><input type="submit" value="Delete" class="del"></form></li>
                            </ul>
                            <p class="metadata">By <a href="http://web-01.ahmad-basheer.tech:5000/medflow/users/${a.user_id}" class="${a.user_id}-answer-user-link">username</a> - At <span>${a.created_at.replace("T", " ") + " UTC"}</span> - Updtaed at <span>${a.updated_at.replace("T", " ") + " UTC"}</span></p>
                            <p>${a.body}</p>
                            <div class="comment-stats">
                                <div class="comments" id="${a.id}"></div>
                            </div>
                        </div>
                    `)

                    // Get the answer user
                    const userLink = $(`.${a.user_id}-answer-user-link`);
                    console.log(userLink)
                    $.ajax({
                        url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${a.user_id}`,
                        type: 'GET',
                        success: function (user) {
                            userLink.text(user.first_name + " " + user.last_name);
                        }
                    })
                    // Get answer comments
                    const answerCommentsContainer = $(`#${a.id}`);
                    answerCommentsContainer.css("text-align", "left");
                    $.ajax({
                        url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/answers/${a.id}/comments`,
                        type: 'GET',
                        success: function (comments) {
                            if (comments.length > 0) {
                                for (const com of comments) {
                                    answerCommentsContainer.append(`
                                        <div class="com">
                                            <ul class="options">
                                                <li><a href="http://web-01.ahmad-basheer.tech:5000/medflow/answers/${com.answer_id}/update_comment/${com.id}">Edit</a></li>
                                                <li><form action="http://web-01.ahmad-basheer.tech:5000/medflow/del_acomment/${com.id}" method="post"><input type="submit" value="Delete" class="del"></form></li>
                                            </ul>
                                            <p class="metadata">By <a href="http://web-01.ahmad-basheer.tech:5000/medflow/users/${com.user_id}" class="${com.user_id}-answer-comment-user"></a> - At <span>${com.created_at.replace("T", " ") + " UTC"}</span> - Updtaed at <span>${com.updated_at.replace("T", " ") + " UTC"}</span></p>
                                            <p>${com.body}</p>
                                            <div class="comment-stats">
                                            </div>
                                        </div>
                                    `)
                                    // Get the comment user
                                    const userLink = $(`.${com.user_id}-answer-comment-user`);
                                    $.ajax({
                                        url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${com.user_id}`,
                                        type: 'GET',
                                        success: function (user) {
                                            userLink.text(user.first_name + " " + user.last_name);
                                        }
                                    })
                                }
                             } else {
                                 answerCommentsContainer.text("No comments");
                                 answerCommentsContainer.addClass("center-text");
                             }
                        }
                    })
                }
            } else {
                answersContainer.text("No answers yet");
                answersContainer.addClass("center-text");
            }
        }
    })
})

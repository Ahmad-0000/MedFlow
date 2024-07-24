// Handles questions page

$(function () {
    let regularIndex = 0;
    let searchIndex = 0;
    const questionsContainer = $(".questions");
    const container = $(".container");
    let more = null;
    let searchSentence = null;
    const search = $("#fts");
    let searchContext = false;

    // Conudct a full text search
    search.on('click', function () {
        searchSentence = $("#fts-sentence").val();
        searchContext = true;
        if (!searchSentence) {
            alert("Enter a search sentence first");
        } else {
            const searchData = JSON.stringify({sentence: searchSentence, index: 0});
            $.ajax({
                url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions_fts`,
                type: 'POST',
                data: searchData,
                contentType: 'application/json',
                success: function (questions) {
                        if (questions.length > 0) { // there is a search result
                            questionsContainer.css("text-align", "left");
                            more = $("#more");
                            if (questions.length > 4) {
                                more.text("More ...");
                            } else {
                                more.text("");
                            }
                            questionsContainer.html("");
                            for (const q of questions) {
                                questionsContainer.append(`
                                <div class="question">
                                    <h4><a href="questions/${q.id}" class="question-link">${q.title}</a></h4>
                                    <p class="question-metadata">
                                        By <span class="user_name"><a href="#" class="${q.user_id}-user-link">${q.user}</a></span> at <span class="created_at">${q.created_at.replace("T", " ") + " UTC"}</span>
                                        - Updated at <span class="updated_at">${q.updated_at.replace("T", " ") + " UTC"}</span>
                                    </p>
                                </div>`)
                                $.ajax({ // Populating the user name part of the question
                                    url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${q.user_id}`,
                                    type: 'GET',
                                    success: function (user) {
                                        const userLink = $(`.${q.user_id}-user-link`);
                                        userLink.text(user.first_name + " " + user.last_name);
                                        userLink.attr("href", `http://web-01.ahmad-basheer.tech:5000/medflow/users/${user.id}`)
                                    }
                                });
                            }
                        } else {
                            questionsContainer.text("No result found");
                            questionsContainer.css("text-align", "center");
                            more = $("#more");
                            more.text("")
                        }
                    }
            })
        }
    })

    // Populates main question page (With no search)
    $.ajax({
        url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${regularIndex}`,
        type: 'GET',
        success: function (questions) {
            if (questions.length > 0) {
                for (let q of questions) {
                    questionsContainer.append(`
                        <div class="question">
                            <h4><a href="questions/${q.id}" class="question-link">${q.title}</a></h4>
                            <p class="question-metadata">
                                By <span class="user_name"><a href="#" class="${q.user_id}-user-link">${q.user}</a></span> at <span class="created_at">${q.created_at.replace("T", " ") + " UTC"}</span>
                                - Updated at <span class="updated_at">${q.updated_at.replace("T", " ") + " UTC"}</span>
                            </p>
                        </div>`)
                        $.ajax({
                            url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${q.user_id}`,
                            type: 'GET',
                            success: function (user) { // Populate user name part of the question
                                const userLink = $(`.${q.user_id}-user-link`);
                                userLink.text(user.first_name + " " + user.last_name);
                                userLink.attr("href", `http://web-01.ahmad-basheer.tech:5000/medflow/users/${user.id}`)
                            }
                        });
                }
                container.append('<span id="more">More ...</span>')
                more = $("#more");
                // Fetch more 5 questions from the api if any
                more.on('click', function () {
                    if (!searchContext) { // Bring arbitrary questions
                        regularIndex += 5;
                        $.ajax({
                            url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions/${regularIndex}`,
                            type: 'GET',
                            success: function (questions) {
                                if (questions.length > 0) {
                                    for (let q of questions) {
                                        questionsContainer.append(`
                                            <div class="question">
                                                <h4><a href="questions/${q.id}" class="question-link">${q.title}</a></h4>
                                                <p class="question-metadata">
                                                    By <span class="user_name"><a href="#" class="${q.user_id}-user-link"></a></span> at <span class="question-date">${q.created_at.replace("T", " ") + " UTC"}</span>
                                                    - Updated at <span class="question-update">${q.updated_at.replace("T", " ") + " UTC"}</span>
                                                </p>
                                            </div>`)
                                        $.ajax({
                                            url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${q.user_id}`,
                                            type: 'GET',
                                            success: function (user) {
                                                const userLink = $(`.${q.user_id}-user-link`);
                                                userLink.text(user.first_name + " " + user.last_name);
                                                userLink.attr("href", `http://web-01.ahmad-basheer.tech:5000/medflow/users/${user.id}`)
                                            }
                                        })
                                    }
                            } else {
                                alert("No more questions");
                            }
                        }
                    })
                    } else { // Conduct a full text search
                        if ($("fts-sentence").val() === "") {
                            searchContext = false;
                            searchIndex = 0;
                        }
                        searchIndex += 5;
                        const searchData = JSON.stringify({sentence: searchSentence, index: searchIndex});
                        $.ajax({
                            url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/questions_fts`,
                            type: 'POST',
                            data: searchData,
                            contentType: 'application/json',
                            success: function (questions) {
                                    if (questions.length > 0) {
                                        questionsContainer.css("text-align", "left");
                                        for (const q of questions) {
                                            questionsContainer.append(`
                                            <div class="question">
                                                <h4><a href="questions/${q.id}" class="question-link">${q.title}</a></h4>
                                                <p class="question-metadata">
                                                    By <span class="user_name"><a href="#" class="${q.user_id}-user-link">${q.user}</a></span> at <span class="created_at">${q.created_at.replace("T", " ") + " UTC"}</span>
                                                    - Updated at <span class="updated_at">${q.updated_at.replace("T", " ") + " UTC"}</span>
                                                </p>
                                            </div>`)
                                            $.ajax({ // Populates user name part of the question
                                                url: `http://web-01.ahmad-basheer.tech:8080/medflow/api/v1/users/${q.user_id}`,
                                                type: 'GET',
                                                success: function (user) {
                                                    const userLink = $(`.${q.user_id}-user-link`);
                                                    userLink.text(user.first_name + " " + user.last_name);
                                                    userLink.attr("href", `http://web-01.ahmad-basheer.tech:5000/medflow/users/${user.id}`)
                                                }
                                            });
                                        }
                                    } else {
                                        alert("No more search results");
                                        searchIndex = 0;
                                    }
                                }
                        })
                    }
                })
            } else {
                questionsContainer.text("No questions");
                questionsContainer.addClass("center-text");
            }
        }
    })
})
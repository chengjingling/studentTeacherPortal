function createAppUser(event) {
    event.preventDefault();
    var form = document.getElementById("createAppUserForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/app_user/0";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("User registered! Please log in.");
            window.location.href = "/login";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("POST", url, true);
    request.send(formData);
}

function writeAppUserDetails(id) {
    var request = new XMLHttpRequest();
    var url = "/api/app_user/" + id;
    var alertShown = false;
    request.onreadystatechange = function() {
        var containerLeft = document.getElementById("containerLeft");
        var containerRight = document.getElementById("containerRight");
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            containerLeft.innerHTML = "<img src='" + data.photo + "' width='400'>";
            if (data.type == "student") {
                var name = "<h1>Student: " + data.first_name + " " + data.last_name + "</h1>";
            }
            else {
                var name = "<h1>Teacher: " + data.first_name + " " + data.last_name + "</h1>";
            }
            containerRight.innerHTML = name;
            containerRight.innerHTML += "ID: " + data.id + "<br>Email: " + data.email;
            var deleteStudentDiv = document.getElementById("deleteStudentDiv");
            if (data.type == "student") {
                deleteStudentDiv.innerHTML = "<button onclick='confirmDeleteStudent(" + id + ")'>Delete</button>";
            }
            else {
                deleteStudentDiv.innerHTML = "";
            }
        }
        else if (JSON.parse(this.responseText) == "app user does not exist") {
            containerLeft.textContent = "User does not exist.";
            containerRight.textContent = "";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function deleteAppUser(id, type) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/app_user/" + id;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            if (type == "student") {
                alert("Student deleted!");
                window.location.href = "/search_students";
            }
            else {
                alert("Account deleted!");
                window.location.href = "/login";
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("DELETE", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
    request.send();
}

function createCourse(event) {
    event.preventDefault();
    var form = document.getElementById("createCourseForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/course/CM0000";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Course created!");
            window.location.href = "/my_courses/" + formData.get("code");
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            if (JSON.parse(this.responseText) == "code exists") {
                alert("Code already exists. Please choose a different one.");
            }
            else {
                alert("Something went wrong, please try again.");
            }
            alertShown = true;
        }
    }
    request.open("POST", url, true);
    request.send(formData);
}

function writeCourseDetails(code) {
    var request = new XMLHttpRequest();
    var url = "/api/course/" + code;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var heading = document.getElementById("heading");
            heading.textContent = data.code + " " + data.name;
            var teacher = document.getElementById("teacher");
            teacher.innerHTML = "<a href='/search_teachers/" + data.teacher.id + "'>" + data.teacher.first_name + " " + data.teacher.last_name + "</a>";
            var description = document.getElementById("description");
            description.textContent = data.description;
            if (data.app_user.type == "teacher") {
                var students = document.getElementById("students");
                if (data.students.length == 0) {
                    students.textContent = "There are no students.";
                }
                else {
                    var studentTable = document.createElement("table");
                    data.students.forEach(function(student) {
                        var tr = document.createElement("tr");
                        var td1 = document.createElement("td");
                        td1.innerHTML = "<a href='/search_students/" + student.id + "'>" + student.first_name + " " + student.last_name + "</a>";
                        tr.append(td1);
                        var td2 = document.createElement("td");
                        var button = document.createElement("button");
                        button.onclick = function() {
                            confirmRemoveStudent(data.code, student.id);
                        }
                        button.textContent = "Remove";
                        td2.append(button);
                        tr.append(td2);
                        studentTable.append(tr);
                    });
                    students.innerHTML = "";
                    students.append(studentTable);
                }
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
    writeMaterials(code);
    writeFeedbacks(code);
}

function updateCourse(event, code) {
    event.preventDefault();
    var form = document.getElementById("updateCourseForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/course/" + code;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Course updated!");
            window.location.href = "/my_courses/" + formData.get("code");
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            if (JSON.parse(this.responseText) == "code exists") {
                alert("Code already exists. Please choose a different one.");
            }
            else {
                alert("Something went wrong, please try again.");
            }
            alertShown = true;
        }
    }
    request.open("PUT", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send(formData);
}

function deleteCourse(code) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/course/" + code;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Course deleted!");
            window.location.href = "/my_courses";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("DELETE", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send();
}

function createMaterial(event, code) {
    event.preventDefault();
    var form = document.getElementById("createMaterialForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/material/" + code + "/0";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Material uploaded!");
            window.location.href = "/my_courses/" + code;
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("POST", url, true);
    request.send(formData);
}

function writeMaterials(code) {
    var request = new XMLHttpRequest();
    var url = "/api/material/" + code + "/0";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var materials = document.getElementById("materials");
            if (data.materials.length == 0) {
                materials.textContent = "There are no materials.";
            }
            else {
                var materialTable = document.createElement("table");
                data.materials.forEach(function(material) {
                    var tr = document.createElement("tr");
                    var td1 = document.createElement("td");
                    td1.innerHTML = "<a href='/my_courses/" + material.course.code + "/" + material.filename + "/view' target='_blank'>" + material.filename + "</a>";
                    tr.append(td1);
                    if (data.app_user.id == material.course.teacher.id) {
                        var td2 = document.createElement("td");
                        var button = document.createElement("button");
                        button.onclick = function() {
                            confirmDeleteMaterial(material.course.code, material.id);
                        }
                        button.textContent = "Delete";
                        td2.append(button);
                        tr.append(td2);
                    }
                    materialTable.append(tr);
                });
                materials.innerHTML = "";
                materials.append(materialTable);
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function deleteMaterial(code, id) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/material/CM0000/" + id;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Material deleted!");
            window.location.href = "/my_courses/" + code;
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("DELETE", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send();
}

function createFeedback(event) {
    event.preventDefault();
    var form = document.getElementById("createFeedbackForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/feedback/0";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Feedback submitted!");
            window.location.href = "/feedback";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("POST", url, true);
    request.send(formData);
}

function writeFeedbacks(code) {
    var request = new XMLHttpRequest();
    var url = "/api/feedback/" + code;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var feedbacks = document.getElementById("feedbacks");
            if (data.length == 0) {
                feedbacks.textContent = "There is no feedback.";
                feedbacks.classList.remove("box");
            }
            else {
                feedbacks.innerHTML = "";
                data.forEach(function(feedback, index, array) {
                    feedbacks.innerHTML += "<a href='/search_students/" + feedback.student.id + "'>" + feedback.student.first_name + " " + feedback.student.last_name + "</a><br>" + feedback.description;
                    if (index != array.length - 1) {
                        feedbacks.innerHTML += "<hr>";
                    }
                });
                feedbacks.classList.add("box");
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function createStatus(event) {
    event.preventDefault();
    var form = document.getElementById("createStatusForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/status";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Status posted!");
            window.location.href = "/";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("POST", url, true);
    request.send(formData);
}

function writeStatuses() {
    var request = new XMLHttpRequest();
    var url = "/api/status";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var statuses = document.getElementById("statuses");
            if (data.length == 0) {
                statuses.textContent = "There are no status posts.";
                statuses.classList.remove("box");
            }
            else {
                statuses.innerHTML = "";
                data.forEach(function(status, index, array) {
                    statuses.innerHTML += "<a href='/search_students/" + status.student.id + "'>" + status.student.first_name + " " + status.student.last_name + "</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class='status-timestamp'>" + status.formatted_timestamp + "</span><br>" + status.description;
                    if (index != array.length - 1) {
                        statuses.innerHTML += "<hr>";
                    }
                });
                statuses.classList.add("box");
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function createChat(event) {
    event.preventDefault();
    var form = document.getElementById("createChatForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/chat/room_name";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            window.location.href = "/chats/" + formData.get("room_name");
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            if (JSON.parse(this.responseText) == "room name exists") {
                alert("Room name already exists. Please choose a different one.");
            }
            else {
                alert("Something went wrong, please try again.");
            }
            alertShown = true;
        }
    }
    request.open("POST", url, true);
    request.send(formData);
}

function writeChat(roomName) {
    var request = new XMLHttpRequest();
    var url = "/api/chat/" + roomName;
    var alertShown = false;
    request.onreadystatechange = function() {
        var chat = document.getElementById("chat");
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            chat.innerHTML = "";
            chat.innerHTML += "<h1>" + roomName + "</h1>";
            if (data.chat_log) {
                chat.innerHTML += "<textarea cols='100' rows='20' readonly>" + data.chat_log + "</textarea><br>";
            }
            else {
                chat.innerHTML += "<textarea cols='100' rows='20' readonly></textarea><br>";
            }
            chat.innerHTML += "<input type='text' size='100' id='messageInput'>";
            chat.innerHTML += "<button id='sendButton'>Send</button>";
            chat.innerHTML += "<h2>Members</h2>";
            chat.innerHTML += "<ul>";
            chat.innerHTML += "<li>" + data.admin.first_name + " " + data.admin.last_name + " (admin)</li>";
            for (var i = 0; i < data.members.length; i++) {
                if (data.members[i].id != data.admin.id) {
                    chat.innerHTML += "<li>" + data.members[i].first_name + " " + data.members[i].last_name + "</li>";
                }
            }
            chat.innerHTML += "</ul><br>";
            var button = document.createElement("button");
            if (data.admin.id == data.app_user.id) {
                button.onclick = function() {
                    confirmDeleteChat(roomName);
                }
                button.textContent = "Delete Chat";
            }
            else {
                button.onclick = function() {
                    confirmLeaveChat(roomName);
                }
                button.textContent = "Leave Chat";
            }
            chat.append(button);
            configureWebsocket(roomName, data.app_user);
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            if (JSON.parse(this.responseText) == "chat does not exist") {
                chat.innerHTML = "<br>Chat does not exist.";
            }
            else {
                alert("Something went wrong, please try again.");
            }
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function updateChat(roomName, message) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    formData.append("message", message);
    var request = new XMLHttpRequest();
    var url = "/api/chat/" + roomName;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            window.location.href = "/chats/" + roomName;
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("PUT", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send(formData);
}

function deleteChat(roomName) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/chat/" + roomName;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Chat deleted!");
            window.location.href = "/chats";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("DELETE", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send();
}

function writeEnrolNotifications() {
    var request = new XMLHttpRequest();
    var url = "/api/enrol_notification/0";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var notifications = document.getElementById("notifications");
            if (data.length == 0) {
                notifications.textContent = "You have no notifications.";
                notifications.classList.remove("box");
            }
            else {
                notifications.innerHTML = "";
                data.forEach(function(notification, index, array) {
                    if (notification.read) {
                        notifications.innerHTML += "<a href='/search_students/" + notification.student.id + "'>" + notification.student.first_name + " " + notification.student.last_name + "</a> has enrolled to " + notification.course.code + " " + notification.course.name + ".";
                    }
                    else {
                        notifications.innerHTML += "<b><a href='/search_students/" + notification.student.id + "'>" + notification.student.first_name + " " + notification.student.last_name + "</a> has enrolled to " + notification.course.code + " " + notification.course.name + ".</b>";
                        notifications.innerHTML += "<button onclick='updateEnrolNotification(" + notification.id + ")' class='mark-as-read-button'>Mark as Read</button>";
                    }
                    if (index != array.length - 1) {
                        notifications.innerHTML += "<hr>";
                    }
                });
                notifications.classList.add("box");
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function updateEnrolNotification(id) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/enrol_notification/" + id;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            window.location.href = "/notifications";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("PUT", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send(formData);
}

function writeMaterialNotifications() {
    var request = new XMLHttpRequest();
    var url = "/api/material_notification/0";
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var notifications = document.getElementById("notifications");
            if (data.length == 0) {
                notifications.textContent = "You have no notifications.";
                notifications.classList.remove("box");
            }
            else {
                notifications.innerHTML = "";
                data.forEach(function(notification, index, array) {
                    if (notification.read) {
                        notifications.innerHTML += notification.material.filename + " has been uploaded to " + notification.material.course.code + " " + notification.material.course.name + ".";
                    }
                    else {
                        notifications.innerHTML += "<b>" + notification.material.filename + " has been uploaded to " + notification.material.course.code + " " + notification.material.course.name + ".</b>";
                        notifications.innerHTML += "<button onclick='updateMaterialNotification(" + notification.id + ")' class='mark-as-read-button'>Mark as Read</button>";
                    }
                    if (index != array.length - 1) {
                        notifications.innerHTML += "<hr>";
                    }
                });
                notifications.classList.add("box");
            }
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("GET", url, true);
    request.send();
}

function updateMaterialNotification(id) {
    var form = document.getElementById("csrfTokenForm");
    var formData = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/material_notification/" + id;
    var alertShown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            window.location.href = "/notifications";
        }
        else if (((this.status > 0 && this.status < 200) || this.status >= 400) && !alertShown) {
            alert("Something went wrong, please try again.");
            alertShown = true;
        }
    }
    request.open("PUT", url, true);
    request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); 
    request.send(formData);
}

function configureWebsocket(roomName, appUser) {
    var roomNameUnderscore = roomName.replace(/ /g, "_");
    var chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomNameUnderscore);
    var messageInput = document.getElementById("messageInput");
    var sendButton = document.getElementById("sendButton");

    messageInput.focus();

    chatSocket.onmessage = function(event) {
        var message = JSON.parse(event.data).message;
        updateChat(roomName, message);
    }

    chatSocket.onclose = function() {
        console.error("Chat socket closed unexpectedly");
    }

    messageInput.onkeyup = function(event) {
        if (event.keyCode == 13) {
            sendButton.click();
        }
    }

    sendButton.onclick = function() {
        chatSocket.send(JSON.stringify({
            "message": messageInput.value
        }));
        messageInput.value = "";
    }
}

function confirmDeleteChat(roomName) {
    if (confirm("Are you sure you want to delete this chat?")) {
        deleteChat(roomName);
    }
}

function confirmLeaveChat(roomName) {
    if (confirm("Are you sure you want to leave this chat?")) {
        window.location.href = "/chats/" + roomName + "/leave";
    }
}

function confirmDeleteStudent(id) {
    if (confirm("Are you sure you want to delete this student?")) {
        deleteAppUser(id, "student");
    }
}

function confirmDeleteMaterial(code, id) {
    if (confirm("Are you sure you want to delete this material?")) {
        deleteMaterial(code, id);
    }
}

function confirmUnenrol(code) {
    if (confirm("Are you sure you want to unenrol from this course?")) {
        window.location.href = "/my_courses/" + code + "/unenrol";
    }
}

function confirmRemoveStudent(code, id) {
    if (confirm("Are you sure you want to remove this student?")) {
        window.location.href="/my_courses/" + code + "/" + id + "/remove";
    }
}

function confirmDeleteCourse(code) {
    if (confirm("Are you sure you want to delete this course?")) {
        deleteCourse(code);
    }
}

function confirmDeleteAccount(id) {
    if (confirm("Are you sure you want to delete this account?\nThis action cannot be undone.")) {
        deleteAppUser(id, "account");
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.querySelector("#search-form");
    if (searchForm) {
        searchForm.addEventListener("submit", (e) => {
            const studentID = document.querySelector("#student_id").value.trim();
            if (!studentID) {
                e.preventDefault();
                alert("請輸入學生學號！");
            }
        });
    }
});
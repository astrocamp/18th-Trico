export function init() {

    const getCSRFToken = () => {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    };

    // 改用事件委派並檢查事件來源
    document.body.addEventListener("click", function (event) {
        if (event.target.closest("[id^='toggle-like-btn-']")) {
            event.preventDefault();
            event.stopPropagation();

            const button = event.target.closest("[id^='toggle-like-btn-']");
            const serviceId = button.getAttribute("data-service-id");
            const url = `/services/like/${serviceId}/`;
            const likeIcons = document.querySelectorAll(`#like-icon-${serviceId}`);
            const csrftoken = getCSRFToken();

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    const newSrc = data?.is_liked ?
                    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' fill='%231C274C' viewBox='0 0 24 24'><path d='M2 9.1371C2 14 6.01943 16.5914 8.96173 18.9109C10 19.7294 11 20.5 12 20.5C13 20.5 14 19.7294 15.0383 18.9109C17.9806 16.5914 22 14 22 9.1371C22 4.27416 16.4998 0.825464 12 5.50063C7.50016 0.825464 2 4.27416 2 9.1371Z'/></svg>"
                    :
                    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' fill='none' stroke='%231C274C' stroke-width='2' viewBox='0 0 24 24'><path d='M12 20.5C11 20.5 10 19.7294 8.96173 18.9109C6.01943 16.5914 2 14 2 9.1371C2 4.27416 7.50016 0.825464 12 5.50063C16.4998 0.825464 22 4.27416 22 9.1371C22 14 17.9806 16.5914 15.0383 18.9109C14 19.7294 13 20.5 12 20.5Z'/></svg>";                

                    likeIcons.forEach((likeIcon) => {
                        likeIcon.setAttribute("src", newSrc);
                    });
                })
                .catch((error) => console.error("Error:", error));
        }
    });
}

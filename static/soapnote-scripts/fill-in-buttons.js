/**
 * Adds text to a text area given the ID of the textbox and the text added
 * @param text The text to add
 * @param textAreaId The ID of the text area
 */
const addFillInText = (text, textAreaId) => {
    const textarea = document.getElementById(textAreaId)

    if (textarea.value === '')
    {
        textarea.value += text
        return
    }

    textarea.value += ` + ${text}`;
}
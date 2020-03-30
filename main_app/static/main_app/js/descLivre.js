function setStars(note)
{
    for (let i = 1; i <= note; i++)
    {
        document.getElementById("star" + i).className += " gold";
    }
}
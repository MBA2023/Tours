"use strict;"

class Schedule {
    constructor(availableTimes, freeSlots, maxParticipants, bookPageUrl) {
        this.availableTimes = availableTimes
        this.freeSlots = freeSlots
        this.maxParticipants = maxParticipants
        this.bookPageUrl = bookPageUrl
        this.container = document.getElementById('schedule')
        this.currenDate = new Date()
        this.picker = datepicker('#schedule__datepicker', {
            minDate: this.currenDate,
            alwaysShow: true,
            onSelect: instance => {
                this.currenDate = instance.dateSelected
                this.render()
            },
        })
        this.picker.setDate(this.currenDate)
        this.picker.show()

    }

    getCurrentDate() {
        return this.currenDate.toISOString().split('T')[0]
    }

    getReservedCurrentTimes() {
        return this.freeSlots[this.getCurrentDate()] || []
    }

    getSlotHtml(availableTime, freePlaces) {
        const slotDiv = document.createElement('div')
        slotDiv.className = 'schedule__slot'
        const slotTime = document.createElement('div')
        slotTime.innerHTML = availableTime
        const reserveBtn = document.createElement('div')
        const places = document.createElement('div')
        const bookDatetime = `${this.getCurrentDate()}T${availableTime}`
        console.log(freePlaces)
        if (freePlaces > 0) {
            reserveBtn.innerHTML = `<a href="${this.bookPageUrl}?d=${bookDatetime}"><button type="button" class="btn btn-success btn-sm">Забронировать</button></a>`
            places.innerHTML = `<span class="badge rounded-pill bg-danger">${freePlaces}</span>`
        } else {
            reserveBtn.innerHTML = '<span class="badge bg-light text-dark">Нет свободных мест</span>'
        }
        slotDiv.appendChild(slotTime, reserveBtn, places)
        slotDiv.appendChild(reserveBtn)
        slotDiv.appendChild(places)
        return slotDiv
    }


    render() {
        const ul = document.createElement('ul')
        ul.className = 'list-group'
        for (let availableTime of  this.availableTimes) {
            const currentFree = this.getReservedCurrentTimes() || {}
            const freePlaces = currentFree[availableTime] !== undefined ? currentFree[availableTime] : this.maxParticipants
            const li = document.createElement('li')
            li.className = 'list-group-item'
            li.appendChild(this.getSlotHtml(availableTime, freePlaces))
            ul.appendChild(li)
        }
        this.container.querySelector('#schedule__timeList').innerHTML = ''
        this.container.querySelector('#schedule__timeList').appendChild(ul)
    }
}
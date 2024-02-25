require "json"
require "date"

def collect
    user = User.first
    comic = Comic.find 5
    colls = [
        {
          volume:16,
          date:"2023-12-10"
        },
        {
          volume:18,
          date:"2023-12-10"
        },
        {
          volume:20,
          date:"2023-12-10"
        },
        {
          volume:1,
          date:"2022-07-28"
        },
        {
          volume:2,
          date:"2022-08-06"
        },
        {
          volume:3,
          date:"2022-10-21"
        },
        {
          volume:4,
          date:"2023-01-07"
        },
        {
          volume:5,
          date:"2023-01-07"
        },
        {
          volume:6,
          date:"2023-04-04"
        },
        {
          volume:7,
          date:"2023-01-07"
        },
        {
          volume:9,
          date:"2023-04-04"
        },
        {
          volume:10,
          date:"2023-05-01"
        },
        {
          volume:11,
          date:"2023-05-01"
        },
        {
          volume:12,
          date:"2023-05-01"
        },
        {
          volume:8,
          date:"2023-04-04"
        },
        {
          volume:14,
          date:"2023-07-09"
        },
        {
          volume:13,
          date:"2023-07-09"
        },
        {
          volume:15,
          date:"2023-07-10"
        },
        {
          volume:17,
          date:"2023-09-04"
        },
        {
          volume:19,
          date:"2023-09-04"
        }
    ]

    colls.each do |c|
        issue = comic.issues.find_by(issue_number: c[:volume])
        date = Date.parse(c[:date])
        CollectedIssue.create(user:, issue:, collected_on: date)
    end
end
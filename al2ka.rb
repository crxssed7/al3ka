require "net/http"
require "json"
require "time"
require "debug"

def make_al_request(media_id, page: 1)
    uri = URI("https://graphql.anilist.co/")
    query = <<-EOF
    query ($mediaId: Int, $page: Int) {
        Page(page: $page, perPage: 500) {
                activities(userId: 5613718, mediaId: $mediaId) {
                ... on ListActivity {
                    createdAt
                    media {
                        title {
                            userPreferred
                        }
                    }
                    status
                    progress
                }
            }
        }
    }
    EOF
    variables = {
        mediaId: media_id,
        page:
    }
    data = {
        query:,
        variables:
    }
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true

    request = Net::HTTP::Post.new(uri.path, {'Content-Type' => 'application/json'})
    request.body = data.to_json

    http.request(request)
end

def check_overlaps(a, b)
    a.each do |i|
        if b.include?(i)
            return true
        end
    end
    false
end

def create_read_issues(kaboom_id, results)
    user = User.first
    comic = Comic.find(kaboom_id)
    ris = []
    comic.ordered_issues.each_with_index do |issue, index|
        result = results[index]
        next unless result
        read_at = result[:finished_reading]
        ris << ReadIssue.new(user:, issue:, read_at: )
    end
    ris
end

def main
    volumes = []

    kaboom_id = 56
    uri = URI("https://raw.githubusercontent.com/crxssed7/al3ka/main/json/Saiki.json")
    response = Net::HTTP.get_response(uri)
    return unless response.is_a? Net::HTTPSuccess

    json = JSON.parse(response.body)
    media_id = json["id"]
    volumes = json["volumes"]

    al_response = make_al_request(media_id)
    return unless al_response.is_a? Net::HTTPSuccess

    al_json = JSON.parse(al_response.body)
    activities = al_json["data"]["Page"]["activities"]

    results = []
    volumes.each_with_index do |volume, index|
        volume_start = volume["start"]
        volume_end = volume["end"]
        started_reading = nil
        finished_reading = nil

        activities.each do |activity|
            created = activity["createdAt"]

            if volume == volumes.last && activity["status"] == "completed"
                if started_reading == nil
                    started_reading = created
                elsif created < started_reading
                    started_reading = created
                end

                if finished_reading == nil
                    finished_reading = created
                elsif created > finished_reading
                    finished_reading = created
                end

                next
            end

            next if activity["status"] != "read chapter"

            regex = /(\d+)/
            match = activity["progress"].scan(regex).flatten
            next unless match.any?

            my_start = match[0].to_i
            my_end = match[-1].to_i
            
            if check_overlaps((volume_start..volume_end).to_a, (my_start..my_end).to_a)
                if started_reading == nil
                    started_reading = created
                elsif created < started_reading
                    started_reading = created
                end

                if finished_reading == nil
                    finished_reading = created
                elsif created > finished_reading
                    finished_reading = created
                end
            end
        end

        results << {volume: index + 1, started_reading: Time.at(started_reading).utc, finished_reading: Time.at(finished_reading).utc}
    end

    create_read_issues(kaboom_id, results)
end

def visual
    main.map { [_1.read_at, _1.issue.issue_number] }
end
local label = script.Parent
label.BackgroundTransparency = 1
label.Visible = false
label.ImageRectSize = FRAME_SIZE

local frames = {}
local pos = Vector2.new(0, 0)
for _ = 1, FRAMES do
	table.insert(frames, pos)

	pos = Vector2.new(pos.X + FRAME_SIZE.X, pos.Y)

	if (pos.X > IMAGE_SIZE.X - FRAME_SIZE.X) then
		pos = Vector2.new(0, pos.Y + FRAME_SIZE.Y)
	end
end

game:GetService("ContentProvider"):PreloadAsync({label})
label.Visible = true

repeat
	for _, frame in ipairs(frames) do
		label.ImageRectOffset = frame
		task.wait(1 / FPS)
	end
until not SHOULD_IMAGE_LOOP
